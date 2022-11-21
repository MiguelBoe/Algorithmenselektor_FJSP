import copy
from dataclasses import dataclass, field
from scheduling_giffler_thompson import get_predecessor
from typing import Dict
from utils import topological_sort_earliest_start

@dataclass
class NeighborhoodSolution:
    schedule: Dict = field(default_factory=lambda: {})
    makespan: int = field(default=0)
    arc: Dict = field(default_factory=lambda: {})

class NeighborHood:
    def __init__(self, init_solution, critical_path, tabu_list):
        self.init_solution = copy.deepcopy(init_solution)
        self.current_solution = {}
        self.neighborhood = {}
        self.tabu_list = tabu_list
        self.critical_path = critical_path
        self.disjunctive_arcs = self.get_disjunctive_arcs()

    def get_disjunctive_arcs(self):
        critical_operations = self.critical_path.copy()
        keys = list(critical_operations.keys())
        disjunctive_arcs = []

        for i in keys:
            for j in keys:
                if critical_operations[i].machine_id == critical_operations[j].machine_id and \
                        ((critical_operations[i].task_on_machine_idx == critical_operations[j].task_on_machine_idx - 1) or \
                         (critical_operations[i].task_on_machine_idx == critical_operations[j].task_on_machine_idx + 1)):
                    disjunctive_arcs.append([i, j])
            keys.remove(i)

        current_tabu_list = self.tabu_list
        for list_entry in range(len(current_tabu_list)): current_tabu_list.append([current_tabu_list[list_entry][1], current_tabu_list[list_entry][0]])
        disjunctive_arcs = list(set(tuple(x) for x in disjunctive_arcs) - set(tuple(x) for x in current_tabu_list))

        return disjunctive_arcs

    def get_neighborhood(self):
        for arc in range(len(self.disjunctive_arcs)):
            self.current_solution = copy.deepcopy(self.init_solution)
            self.swap(arc)
            self.get_earliest_start()
            self.create_neighborhood(arc)
        return self.neighborhood

    def swap(self, arc):
        i, j = self.disjunctive_arcs[arc][0], self.disjunctive_arcs[arc][1]
        self.current_solution[i].task_on_machine_idx, self.current_solution[j].task_on_machine_idx = self.current_solution[j].task_on_machine_idx, self.current_solution[i].task_on_machine_idx
        new_order = list(self.current_solution.keys())
        a, b = new_order.index(i), new_order.index(j)
        new_order[b], new_order[a] = new_order[a], new_order[b]
        self.current_solution = {k: self.current_solution[k] for k in new_order}

        current_arc = [i, j]
        for operation in list(self.current_solution.keys()):
            if i in self.current_solution[operation].pred or j in self.current_solution[operation].pred:
                current_arc.append(operation)
        current_arc = set(current_arc)

        for i in current_arc:
            self.current_solution[i].pred = get_predecessor(schedule=self.current_solution,
                                                        task_id=self.current_solution[i].task_id,
                                                        task_on_machine_idx=self.current_solution[i].task_on_machine_idx,
                                                        machine_id=self.current_solution[i].machine_id,
                                                        job_id=self.current_solution[i].job_id)

    def get_earliest_start(self):
        new_topological_order = topological_sort_earliest_start(self.current_solution)
        for i in new_topological_order:
            pred_start_times = [self.current_solution[x].end for x in self.current_solution[i].pred]
            pred_start_times.append(0)
            self.current_solution[i].start = max(pred_start_times)
            self.current_solution[i].end = self.current_solution[i].start + self.current_solution[i].duration

    def create_neighborhood(self, arc):
        neighbor = NeighborhoodSolution(schedule = self.current_solution, makespan = self.current_solution[max(self.current_solution, key=lambda key: self.current_solution[key].end)].end, arc = self.disjunctive_arcs[arc])
        self.neighborhood.update({arc: neighbor})