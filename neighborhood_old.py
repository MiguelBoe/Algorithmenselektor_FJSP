from scheduling_giffler_thompson import get_predecessor
import copy

def get_neighbor_solution(schedule, critical_path):
    neighbor_solution = copy.deepcopy(schedule)
    disjunctive_arcs = find_disjunctive_arcs(critical_path)

    for arc in list(disjunctive_arcs.keys()):
        keys = swap(neighbor_solution, disjunctive_arcs[arc])
        get_earliest_start(neighbor_solution, keys)

    return neighbor_solution

def find_disjunctive_arcs(critical_path):
    critical_operations = critical_path.copy()
    keys = list(critical_operations.keys())
    disjunctive_arcs = {}
    key = 0

    for i in keys:
        for j in keys:
            if critical_operations[i].machine_id == critical_operations[j].machine_id and \
                    ((critical_operations[i].task_on_machine_idx == critical_operations[j].task_on_machine_idx -1) or \
                    (critical_operations[i].task_on_machine_idx == critical_operations[j].task_on_machine_idx +1)):
                disjunctive_arcs.update({key:{'i':i, 'j':j}})
                print(f'{i} und {j}')
                key = + 1
        keys.remove(i)
    return disjunctive_arcs


def swap(neighbor_solution, arc):
    i = arc['i']
    j = arc['j']
    keys = list(neighbor_solution.keys())
    neighbor_solution[i].task_on_machine_idx, neighbor_solution[j].task_on_machine_idx = neighbor_solution[j].task_on_machine_idx, neighbor_solution[i].task_on_machine_idx
    a, b = keys.index(i), keys.index(j)
    keys[b], keys[a] = keys[a], keys[b]

    for i in list(neighbor_solution.keys()):
        neighbor_solution[i].pred = get_predecessor(schedule=neighbor_solution, task_id=neighbor_solution[i].task_id, task_on_machine_idx=neighbor_solution[i].task_on_machine_idx, machine_id=neighbor_solution[i].machine_id, job_id=neighbor_solution[i].job_id)

    return keys

def get_earliest_start(neighbor_solution, keys):

    for i in keys:
        pred_start_times = [neighbor_solution[x].end for x in neighbor_solution[i].pred]
        pred_start_times.append(0)
        neighbor_solution[i].start = max(pred_start_times)
        neighbor_solution[i].end = neighbor_solution[i].start + neighbor_solution[i].duration