import copy
from dataclasses import dataclass, field
from scheduling_giffler_thompson import get_predecessor
from typing import Dict

@dataclass
class neighborhood_solution:
    schedule: Dict = field(default_factory=lambda: {})
    makespan: int = field(default=0)

class NeighborHood:
    def __init__(self, init_solution, critical_path):
        self.init_solution = copy.deepcopy(init_solution)
        self.current_solution = {}
        self.neighborhood = {}
        self.critical_path = critical_path
        self.disjunctive_arcs = self.get_disjunctive_arcs()

    def get_disjunctive_arcs(self):
        critical_operations = self.critical_path.copy()
        keys = list(critical_operations.keys())
        disjunctive_arcs = {}
        key = 0

        for i in keys:
            for j in keys:
                if critical_operations[i].machine_id == critical_operations[j].machine_id and \
                        ((critical_operations[i].task_on_machine_idx == critical_operations[
                            j].task_on_machine_idx - 1) or \
                         (critical_operations[i].task_on_machine_idx == critical_operations[
                             j].task_on_machine_idx + 1)):
                    disjunctive_arcs.update({key: {'i': i, 'j': j}})
                    key += 1
            keys.remove(i)
        return disjunctive_arcs

    def get_neighborhood(self):
        for arc in list(self.disjunctive_arcs.keys()):
            self.current_solution = copy.deepcopy(self.init_solution)
            self.swap(arc)
            self.get_earliest_start()
            self.create(arc)
        return self.neighborhood

    def swap(self, arc):
        i, j = self.disjunctive_arcs[arc]['i'], self.disjunctive_arcs[arc]['j']
        self.current_solution[i].task_on_machine_idx, self.current_solution[j].task_on_machine_idx = self.current_solution[j].task_on_machine_idx, self.current_solution[i].task_on_machine_idx
        self.current_solution[i], self.current_solution[j] = self.current_solution[j], self.current_solution[i]

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
        for i in list(self.current_solution.keys()):
            pred_start_times = [self.current_solution[x].end for x in self.current_solution[i].pred]
            pred_start_times.append(0)
            self.current_solution[i].start = max(pred_start_times)
            self.current_solution[i].end = self.current_solution[i].start + self.current_solution[i].duration

    def create(self, arc):
        neighbor = neighborhood_solution(schedule = self.current_solution, makespan = self.current_solution[max(self.current_solution, key=lambda key: self.current_solution[key].end)].end)
        self.neighborhood.update({arc: neighbor})