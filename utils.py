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

def get_schedule_list(schedule):
    schedule_list = []
    for k,v in schedule.items():
        schedule_list.append({'Task':v.machine_id, 'Start':v.start, 'Finish':v.end, 'Resource': f'Job_{v.job_id}'})
    return schedule_list

def topologicalSortUtil(v, Stack, visited, adj):
    visited[v] = True
    for i in adj[v]:
        if (not visited[i[0]]):
            topologicalSortUtil(i[0], Stack, visited, adj)
    Stack.append(v)

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