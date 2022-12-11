from giffler_thompson import ScheduledTask

# Diese Funktion dient zur Transformation der Daten (von OR-Tools) für die Visualisierung.
def visualize_schedule(assigned_jobs, all_machines, plan_date):
    schedule_list = []
    for machine in all_machines:
        assigned_jobs[machine].sort()
        for assigned_task in assigned_jobs[machine]:
            name = 'Job_%i' % assigned_task.job
            temp = dict(Task = machine,Start = plan_date + assigned_task.start,
                        Finish = plan_date + assigned_task.start + assigned_task.duration,
                        Resource = name)
            schedule_list.append(temp)
    schedule_list.sort(key = lambda x: x['Task'])
    return schedule_list

# Diese Funktion dient zur Transformation der Daten (von der Metaheuristik) für die Visualisierung.
def get_schedule_list(schedule):
    schedule_list = []
    for k,v in schedule.items():
        schedule_list.append({'Task':v.machine_id, 'Start':v.start, 'Finish':v.end, 'Resource': f'Job_{v.job_id}'})
    schedule_list = sorted(schedule_list, key=lambda x: x['Task'])
    return schedule_list

# Mit dieser Funktion wird die topologische Sortierung der Adjazenzliste vorgenommen.
def topologicalSortUtil(v, Stack, visited, adj):
    visited[v] = True
    for i in adj[v]:
        if (not visited[i[0]]):
            topologicalSortUtil(i[0], Stack, visited, adj)
    Stack.append(v)

# Diese Funktion ist der Funktion zur Berechnung des kritischen Pfades sehr ähnlich. Sie funktioniert allerdings etwas anders und ist nur dafür gedacht, die neue topologische Reihenfolge der Operationen nach einem Move zu ermitteln.
def topological_sort_earliest_start(current_solution):
    V, Stack, visited = len(current_solution), [], [False for i in range(len(current_solution))]
    adj = [[] for i in range(V)]

    for i in list(current_solution.keys()):
        for k in current_solution[i].pred:
            adj[i].append([k, current_solution[i].duration])

    for v in range(V):
        if (visited[v] == False):
            topologicalSortUtil(v, Stack, visited, adj)

    return Stack

# Diese Funktion dient dabei die aktuelle Lösung bei der Suche nach Nachbarschaftslösungen zu kopieren. Diese Funktion zieht zwar sehr viel Zeit im Algorithmus, ist aber die bisher schnellste gefundene Lösung.
def current_solution_create_copy(init_solution):
    current_solution = {}
    for i in init_solution.keys():
        scheduled_task = ScheduledTask(
            machine_id=init_solution[i].machine_id,
            job_id=init_solution[i].job_id,
            duration=init_solution[i].duration,
            task_id=init_solution[i].task_id,
            start=init_solution[i].start,
            end=init_solution[i].end,
            task_on_machine_idx=init_solution[i].task_on_machine_idx,
            pred=init_solution[i].pred
        )
        current_solution.update({i: scheduled_task})

    return current_solution