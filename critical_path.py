def topologicalSortUtil(v, Stack, visited, adj):

    visited[v] = True

    for i in adj[v]:
        if (not visited[i[0]]):
            topologicalSortUtil(i[0])

    Stack.append(v)


def longestPath(end_node, V, Stack, visited, adj, schedule):

    dist = [-10 ** 9 for i in range(V)]

    for v in range(V):
        if (visited[v] == False):
            topologicalSortUtil(v, Stack, visited, adj)

    dist[end_node] = 0

    while (len(Stack) > 0):

        u = Stack[-1]
        del Stack[-1]

        if (dist[u] != 10 ** 9):
            for i in adj[u]:
                if (dist[i[0]] < dist[u] + i[1]):
                    dist[i[0]] = dist[u] + i[1]

    for i in range(V):
        schedule[i].q = dist[i]


def get_earliest_start(schedule):
    for i in list(schedule.keys()):
        pred_start_times=[schedule[x].end for x in schedule[i].pred]
        pred_start_times.append(0)
        schedule[i].r=max(pred_start_times)


def get_critical_path(schedule):
    V, Stack, visited = len(schedule), [], [False for i in range(len(schedule))]
    adj = [[] for i in range(V)]

    get_earliest_start(schedule)

    for i in list(schedule.keys()):
        for k in schedule[i].pred:
            if schedule[i].start == schedule[k].end:
                adj[i].append([k,schedule[i].duration])

    end_node = V-1
    makespan = schedule[end_node].end
    longestPath(end_node, V, Stack, visited, adj, schedule)

    return [v for k, v in schedule.items() if v.r + v.duration + v.q == makespan]
