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
        schedule[i].longest_path = dist[i]


def get_critical_path(schedule):
    V, Stack, visited = len(schedule), [], [False for i in range(len(schedule))]
    adj = [[] for i in range(V)]

    for i in list(schedule.keys()):
        for k in schedule[i].pred:
            if schedule[i].start == schedule[k].end:
                adj[i].append([k,schedule[i].duration])

    end_node = max(schedule, key=lambda key: schedule[key].end)
    makespan = schedule[end_node].end
    longestPath(end_node, V, Stack, visited, adj, schedule)

    return {k:v for k, v in schedule.items() if v.start + v.duration + v.longest_path == makespan}
