"""
@author: böttcher & pretz

#-----------------------------------------------------------------------------#
#         Projektseminar Business Analytics - Wintersemester 22/23            #
#-----------------------------------------------------------------------------#
#                                                                             #
#                            Kritischer Pfad                                  #
#                 Ermittelung der kritischen Operationen                      #
#                                                                             #
#                                                                             #
#-----------------------------------------------------------------------------#
"""

from utils import topologicalSortUtil
from giffler_thompson import ScheduledTask


def get_critical_path(schedule: dict[str, ScheduledTask]) -> dict[str, ScheduledTask]:

    """Berechnen der kritischen Operationen"""

    # Zunächst werden die Operationen in einer Adjazenzliste abgespeichert, um die Vorangsbeziehungen abzuspeichern.
    num_tasks, Stack = len(schedule), []
    adj = [[] for _ in range(num_tasks)]

    # für jeden task im schedule
    for task in list(schedule.keys()):
        # für jeden Vorgänger des tasks (Maschinenvorgänger und JobVorgänger)
        for pred_task in schedule[task].pred:
            # Überprüfen ob kein Puffer zwischen den beiden Tasks ist
            if schedule[task].start == schedule[pred_task].end:
                # Kein Puffer, dann hinzufügen zur Liste
                # warum pred nummer und taskzeit?
                adj[task].append([pred_task, schedule[task].duration])

    # Bestimmung des Endknoten, sowie der makespan.
    end_node = max(schedule, key=lambda key: schedule[key].end)  # schedule[-1]
    makespan = schedule[end_node].end
    # Berechnen der Tailzeit für jeden Vorgang mit der Funktion longestPath.
    longestPath(end_node, num_tasks, Stack, adj, schedule)

    # Es werden nur kritische Operationen zurückgegeben. Dies sind diejenigen Operationen, welche die untenstehende Gleichung erfüllen.
    return {key: task for key, task in schedule.items() if task.start + task.duration + task.longest_path == makespan}


def longestPath(end_node: int, num_tasks: int, Stack: list, adj: list[list], schedule: dict[str:ScheduledTask]):

    """Berechnung des Längstens Pfades"""

    visited = [False for _ in range(len(schedule))]
    # Vorgänge in eine topologische Reihenfolge bringen.
    # Distanz vom Knoten bis zum Ende
    dist = [-(1e6) for _ in range(num_tasks)]
    # Für jeden Task die Topologische Position berechnen
    for task in range(num_tasks):
        if visited[task] == False:
            topologicalSortUtil(task, Stack, visited, adj)
    dist[end_node] = 0

    # Bestimmung längster Wege vom Ausgangsknoten aus.
    # Alle Knoten, welche nicht zum Endknoten führen bleiben bei Distanz von -1e6
    while Stack:
        last_task = Stack[-1]
        del Stack[-1]
        if dist[last_task] != 1e6:
            # Für die Vorgänger des Tasks
            for pred in adj[last_task]:
                # Wenn die 'Distanz des Vorgängers zum EndTask' <  'Distanz des betrachteten Task' + 'Dauer des Vorgängers'
                if dist[pred[0]] < dist[last_task] + pred[1]:
                    dist[pred[0]] = dist[last_task] + pred[1]

    # Für jeden Task die Distanz zum Ende im Schedule abspeichern
    for task in range(num_tasks):
        schedule[task].longest_path = dist[task]


if __name__ == "__main__":

    from jobList import JobList
    from giffler_thompson import giffler_thompson

    instance = [
        [(2, 3), (1, 5), (3, 8), (0, 2)],
        [(0, 6), (1, 4), (2, 2), (3, 5)],
        [(1, 3), (0, 1), (2, 6), (3, 2)],
        [(2, 3), (1, 7), (0, 5), (3, 1)],
        [(3, 3), (2, 4), (1, 1), (0, 6)],
    ]

    jobs_data = JobList(instance)

    prio = "LRPT"  # LPT,SPT,LRPT,SRPT

    schedule = giffler_thompson(jobs_data, prio)

    critical_tasks = get_critical_path(schedule)

    print(critical_tasks)