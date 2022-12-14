from dataclasses import dataclass, field
from giffler_thompson import get_predecessor
from typing import Dict
from utils import topological_sort_earliest_start, current_solution_create_copy

# Generierung eines Objektes zur Speicherung einer Nachbarschaftslösung. Der "Arc" gibt den kritischen Bogen, bzw. den Move an, mit welchem die Nachbarschaft gefunden wurde.
@dataclass
class NeighborhoodSolution:
    schedule: Dict = field(default_factory=lambda: {})
    makespan: int = field(default=0)
    arc: Dict = field(default_factory=lambda: {})

class NeighborHood:
    def __init__(self, init_solution, critical_path, tabu_list, neighborhood_definition):
        self.init_solution = init_solution
        self.current_solution = {}
        self.neighborhood = {}
        self.tabu_list = tabu_list
        self.critical_path = critical_path
        if neighborhood_definition == 1:
            self.disjunctive_arcs = self.neighborhood_definition_N1()
        elif neighborhood_definition == 5:
            self.disjunctive_arcs = self.neighborhood_definition_N5()

    # Mit dieser Funktion werden auf dem jeweiligen kritischen Pfad alle Arcs nach Nachbarschaftsdefinition N1 gefunden.
    def neighborhood_definition_N1(self):
        critical_operations = self.critical_path.copy()
        keys = list(critical_operations.keys())
        disjunctive_arcs = []

        for i in keys:
            for j in keys:
                if critical_operations[i].machine_id == critical_operations[j].machine_id and \
                        ((critical_operations[i].task_on_machine_idx == critical_operations[j].task_on_machine_idx - 1) or \
                         (critical_operations[i].task_on_machine_idx == critical_operations[j].task_on_machine_idx + 1)):
                    disjunctive_arcs.append([[i, j]])
            keys.remove(i)

        current_tabu_list = self.tabu_list.copy()
        disjunctive_arcs = [item for item in disjunctive_arcs if item[0][0] not in current_tabu_list and item[0][1] not in current_tabu_list]

        return disjunctive_arcs

    def neighborhood_definition_N5(self):
        critical_operations = self.critical_path.copy()
        keys = list(critical_operations.keys())
        disjunctive_arcs = []

        for i in keys:
            for j in critical_operations[i].pred:
                if j in keys:
                    if critical_operations[i].job_id == critical_operations[j].job_id:
                        block_j = {k: v for k, v in critical_operations.items() if v.machine_id == critical_operations[j].machine_id}
                        block_i = {k: v for k, v in critical_operations.items() if v.machine_id == critical_operations[i].machine_id}
                        try:
                            pred_j = list({k: v for k, v in block_j.items() if v.end == critical_operations[j].start}.keys())[0]
                            sucs_i = list({k: v for k, v in block_i.items() if v.start == critical_operations[i].end}.keys())[0]
                            disjunctive_arcs.append([[pred_j, j], [i, sucs_i]])
                        except Exception: pass

        current_tabu_list = self.tabu_list.copy()
        disjunctive_arcs = [item for item in disjunctive_arcs if item[0][0] not in current_tabu_list
                            and item[0][1] not in current_tabu_list
                            and item[1][0] not in current_tabu_list
                            and item[1][1] not in current_tabu_list]

        return disjunctive_arcs

    # Dies ist die Hauptfunktion der Nachbarschaftssuche. Hiermit wird die Suche koordiniert. Für jeden gefundenen Arc werden die untenstehenden Schritte ausgeführt.
    def get_neighborhood(self):
        for arc in range(len(self.disjunctive_arcs)):
            self.current_solution = current_solution_create_copy(self.init_solution)  # 1. Als erstes wird eine Kopie erstellt, damit die aktuelle Lösung nicht überschrieben wird. Kostet viel Laufzeit.
            self.swap(arc)                                                            # 2. Als nächstes wird der Swap-Move ausgeführt.
            self.get_release_times()                                                 # 3. Die Startpunkte jeder Operation werden definiert, wodurch zudem der makespan der Lösung definiert werden kann. Kostet viel Laufzeit, sollte jedoch in O(n) sein.
            self.create_neighborhood(arc)                                             # 4. Die Lösung wird in einem Objekt abgespeichert.
        return self.neighborhood                                                      # 5. die gefundene Nachbarschaft wird an die TabuSearch übergeben.

    # In dieser Funktion wird der Swap-Move ausgeführt. Dafür wird die Position der Vorgänge im Dict vertrauscht und die task_on_machine_idx. Zusätzlich werden die Vorgänger Knoten der betroffenen Vorgänge aktualisiert.
    def swap(self, arc):
        # Durchführung des Moves
        for a in self.disjunctive_arcs[arc]:
            i, j = a[0], a[1]
            self.current_solution[i].task_on_machine_idx, self.current_solution[j].task_on_machine_idx = \
            self.current_solution[j].task_on_machine_idx, self.current_solution[i].task_on_machine_idx
            new_order = list(self.current_solution.keys())
            a, b = new_order.index(i), new_order.index(j)
            new_order[b], new_order[a] = new_order[a], new_order[b]
            self.current_solution = {k: self.current_solution[k] for k in new_order}

            # Bestimmung für welche Vorgänge die Vorgänger aktualisiert werden müssen.
            current_arc = [i, j]
            for operation in list(self.current_solution.keys()):
                if i in self.current_solution[operation].pred or j in self.current_solution[operation].pred:
                    current_arc.append(operation)
            current_arc = set(current_arc)

            # Aktualisierung der Vorgänger der betroffenen Vorgänge.
            for i in current_arc:
                self.current_solution[i].pred = get_predecessor(schedule=self.current_solution,
                                                                task_id=self.current_solution[i].task_id,
                                                                task_on_machine_idx=self.current_solution[i].task_on_machine_idx,
                                                                machine_id=self.current_solution[i].machine_id,
                                                                job_id=self.current_solution[i].job_id)

    # Diese Funktion dient dafür die Start- und Endzeitpunkte der Vorgänge zu aktualisiern, um anschließend den neuen makespan zu bestimmen.
    def get_release_times(self):
        # Zunächst müssen dafür die Vorgänge mit Hilfe einer Adjazenzliste in eine topologische Reihenfolge gebracht werden. Dies funktioniert in O(n).
        new_topological_order = topological_sort_earliest_start(self.current_solution)
        #Als nächstes werden die Start- und Endzeitpunkte der Reihe nach aktualisiert. Dies funktioniert ebenfalls in O(n). Demnach liegt die Gesamtlaufzeit der Funktion in O(n).
        for i in new_topological_order:
            pred_start_times = [self.current_solution[x].end for x in self.current_solution[i].pred]
            pred_start_times.append(0)
            self.current_solution[i].start = max(pred_start_times)
            self.current_solution[i].end = self.current_solution[i].start + self.current_solution[i].duration

    # In dieser Funktion werden die Nachbarschafts-Objekte generiert.
    def create_neighborhood(self, arc):
        neighbor = NeighborhoodSolution(schedule = self.current_solution, makespan = self.current_solution[max(self.current_solution, key=lambda key: self.current_solution[key].end)].end, arc = self.disjunctive_arcs[arc])
        self.neighborhood.update({arc: neighbor})