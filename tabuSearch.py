from neighborHood import NeighborHood, NeighborhoodSolution
import plotly.figure_factory as ff
from utils import get_schedule_list
from critical_path import get_critical_path
import time

# Nachfolgend wird die Klasse TabuSearch initilisiert.
class TabuSearch:
    def __init__(self, current_solution, max_iter, tabu_list_length, time_limit_in_seconds):
        self.current_solution = current_solution
        self.best_solutions = {0:NeighborhoodSolution(schedule=current_solution, makespan=current_solution[max(current_solution, key=lambda key: current_solution[key].end)].end, arc=[])}
        self.critical_path = get_critical_path(self.current_solution)
        self.tabu_list_length = tabu_list_length
        self.max_iter = max_iter
        self.time_limit_in_seconds = time_limit_in_seconds
        self.tabu_list = []

    # Mit der Funktion solve() wird die Tabu-Suche gestartet, um eine möglichst gute zulässige Lösung zu finden.
    def solve(self, timeout):
        # Das Verfahren wird max_iter Iterationen lange durchgeführt. Danach wird die beste gefundene Lösung zurückgegeben.
        for i in range(self.max_iter):
            # Als erstes wird die Nachbarschaft basierend auf der aktuellen verwendeten Lösung definiert. Dies geschieht mit der Klasse NeighborHood. Es kann manuel zwischen Nachbarschaftsdefinition N1 und N5 gewechselt werden.
            neighborhood = NeighborHood(init_solution = self.current_solution, critical_path = get_critical_path(self.current_solution), tabu_list = self.tabu_list, neighborhood_definition=1).get_neighborhood()
            # Wenn die Nachbarschaft ausgehend von der aktuellen Lösung leer ist oder die Laufzeitgrenze erreicht wurde, wird das Verfahren abgebrochen und die beste gefundene Lösung wird ausgegeben.
            if neighborhood and time.time() < timeout:
                # Die beste Lösung der Nachbarschaft wird als neue Lösung definiert.
                new_solution = neighborhood[min(neighborhood, key=lambda key: neighborhood[key].makespan)]
                # Der 'move', bzw. der Bogen, mit welcher diese Lösung gefunden wurde, wird auf die Tabu-Liste gesetzt.
                tabu_arc = new_solution.arc
                # Die untenstehenden Objekt-Parameter werden aktualisiert.
                self.current_solution = new_solution.schedule
                self.best_solutions.update({i+1:new_solution})
                self.tabu_list.append([tabu_arc[0][1]])
                self.tabu_list = self.tabu_list[-self.tabu_list_length:]
            else: break
        # Rückgabe der besten gefundenen Lösung.
        return self.best_solutions[min(self.best_solutions, key=lambda key: self.best_solutions[key].makespan)]

    # Der variable_solve funktioniert ähnlich wie der normale solve, außer, dass bei der Erreichung der maximalen Iterationszahl eine andere Nachbarschaftsdefinition gewählt wird.
    def variable_solve(self, timeout):
        # Der Parameter für das Zählen der Iterationen wird initilisiert.
        iteration = 0
        # Das Verfahren wird so lange durchgeführt bis das Laufzeitlimit erreicht wurde.
        while time.time() < timeout:
            # Wenn max_iter Iterationen lang keine bessere Lösung gefunden werden konnte, wird automatisch zu Nachbarschaftsdefiniton N1 gewechselt. Wenn N1 eine bessere Lösung findet, wird wieder N5 benutzt.
            if iteration < self.max_iter:
                neighborhood_definition = 5
            else:
                neighborhood_definition = 1
            # Die Nachbarschaft basierend auf der aktuellen verwendeten Lösung definiert. Dies geschieht mit der Klasse NeighborHood.
            neighborhood = NeighborHood(init_solution=self.current_solution, critical_path=get_critical_path(self.current_solution),tabu_list=self.tabu_list, neighborhood_definition=neighborhood_definition).get_neighborhood()

            # Wenn die Nachbarschaft ausgehend von der aktuellen Lösung leer ist, wird das Verfahren abgebrochen und die beste gefundene Lösung wird ausgegeben.
            if neighborhood:
                # Die beste Lösung der Nachbarschaft wird als neue Lösung definiert.
                new_solution = neighborhood[min(neighborhood, key=lambda key: neighborhood[key].makespan)]
                # Der 'move', bzw. der Bogen, mit welcher diese Lösung gefunden wurde, wird auf die Tabu-Liste gesetzt.
                tabu_arc = new_solution.arc

                # Konnte die beste Lösung verbessert werden, wird der iteration-Parameter auf 0 zurückgesetzt. Konnte die beste Lösung nicht verbessert werden, wird der iteration-Parameter um 1 erhöht. So werden die Nachbarschaftsdefinitionen gesteuert.
                if new_solution.makespan < self.best_solutions[min(self.best_solutions, key=lambda key: self.best_solutions[key].makespan)].makespan:iteration = 0
                elif new_solution.makespan >= self.best_solutions[min(self.best_solutions, key=lambda key: self.best_solutions[key].makespan)].makespan:iteration += 1

                # Die untenstehenden Objekt-Parameter werden aktualisiert.
                self.current_solution = new_solution.schedule
                self.best_solutions.update({list(self.best_solutions)[-1] + 1: new_solution})
                self.tabu_list.append([tabu_arc[0][1]])
                self.tabu_list = self.tabu_list[-self.tabu_list_length:]
            else: iteration = self.max_iter
        # Rückgabe der besten gefundenen Lösung.
        return self.best_solutions[min(self.best_solutions, key=lambda key: self.best_solutions[key].makespan)]