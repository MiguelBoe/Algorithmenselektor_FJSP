from utils import topologicalSortUtil


def longestPath(end_node, V, Stack, visited, adj, schedule):

    # Als erstes werden die Vorgänge in eine topologische Reihenfolge gebracht.
    dist = [-10 ** 9 for i in range(V)]
    for v in range(V):
        if (visited[v] == False):
            topologicalSortUtil(v, Stack, visited, adj)
    dist[end_node] = 0

    # Nach dieser gefundenen Reihenfolge werden längsten Wege vom Ausgangsknoten aus bestimmt. Alle Knoten, welche nicht zum Endknoten führen, werden mit einem hohen negativen Wert bestraft, damit sie in keinem Fall Gleichung zur Identifizierung einer kritischen Operation erfüllen.
    while (len(Stack) > 0):
        u = Stack[-1]
        del Stack[-1]
        if (dist[u] != 10 ** 9):
            for i in adj[u]:
                if (dist[i[0]] < dist[u] + i[1]):
                    dist[i[0]] = dist[u] + i[1]

    for i in range(V):
        schedule[i].longest_path = dist[i]

# Zunächst werden die Operationen in einer Adjazenzliste abgespeichert, um die Vorangsbeziehungen abzuspeichern.
def get_critical_path(schedule):
    V, Stack, visited = len(schedule), [], [False for i in range(len(schedule))]
    adj = [[] for i in range(V)]

    for i in list(schedule.keys()):
        for k in schedule[i].pred:
            if schedule[i].start == schedule[k].end:
                adj[i].append([k,schedule[i].duration])

    # Als nächstes wird der Endknoten bestimmt, sowie der makespan. Danach wird die Tailzeit für jeden Vorgang mit der Funktion longestPath berechnet.
    end_node = max(schedule, key=lambda key: schedule[key].end)
    makespan = schedule[end_node].end
    longestPath(end_node, V, Stack, visited, adj, schedule)

    # Es werden nur kritische Operationen zurückgegeben. Dies sind diejenigen Operationen, welche die untenstehende Gleichung erfüllen.
    return {k:v for k, v in schedule.items() if v.start + v.duration + v.longest_path == makespan}
