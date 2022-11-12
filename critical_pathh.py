def topologicalSortUtil(v, Stack, visited, adj, schedule):
    #global Stack, visited, adj
    visited[v] = True

    # Recur for all the vertices adjacent to this vertex
    # list<AdjListNode>::iterator i
    for i in adj[v]:
        if (not visited[i[0]]):
            topologicalSortUtil(i[0])

    # Push current vertex to stack which stores topological
    # sort
    Stack.append(v)


# The function to find longest distances from a given vertex.
# It uses recursive topologicalSortUtil() to get topological
# sorting.
def longestPath(s, V, Stack, visited, adj, schedule):
    #global Stack, visited, adj, V
    dist = [-10 ** 9 for i in range(V)]

    # Call the recursive helper function to store Topological
    # Sort starting from all vertices one by one
    for i in range(V):
        if (visited[i] == False):
            topologicalSortUtil(i, Stack, visited, adj, schedule)
    # print(Stack)

    # Initialize distances to all vertices as infinite and
    # distance to source as 0
    dist[s] = 0
    # Stack.append(1)

    # Process vertices in topological order
    while (len(Stack) > 0):

        # Get the next vertex from topological order
        u = Stack[-1]
        del Stack[-1]
        # print(u)

        # Update distances of all adjacent vertices
        # list<AdjListNode>::iterator i
        if (dist[u] != 10 ** 9):
            for i in adj[u]:
                # print(u, i)
                if (dist[i[0]] < dist[u] + i[1]):
                    dist[i[0]] = dist[u] + i[1]

    # Print calculated longest distances
    # print(dist)
    for i in range(V):
        print("INF ", end="") if (dist[i] == -10 ** 9) else print(dist[i], end=" ")
        schedule[i].q = dist[i]
    print()


# Driver code
def get_critical_path(schedule):
    V, Stack, visited = len(schedule), [], [False for i in range(16)]
    adj = [[] for i in range(16)]

    for i in list(schedule.keys()):
        for k in schedule[i].pred:
            if schedule[i].start == schedule[k].end:
                adj[i].append([k,schedule[i].duration])

    s = 15
    print("Following are longest distances from source vertex ", s)
    longestPath(s, V, Stack, visited, adj, schedule)
