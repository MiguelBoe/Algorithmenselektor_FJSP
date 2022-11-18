import copy
from neighborHood import NeighborHood
import plotly.figure_factory as ff
from utils import get_schedule_list
from critical_path import get_critical_path

class TabuSearch:
    def __init__(self, current_solution, max_iter, tabu_list_length):
        self.best_solution = copy.deepcopy(current_solution)
        self.critical_path = get_critical_path(self.best_solution)
        self.tabu_list_length = tabu_list_length
        self.max_iter = max_iter
        self.tabu_list = []

    def solve(self):
        for i in range(self.max_iter):
            neighborhood = NeighborHood(init_solution = self.best_solution, critical_path = get_critical_path(self.best_solution), tabu_list = self.tabu_list).get_neighborhood()
            tabu_arc = neighborhood[min(neighborhood, key=lambda key: neighborhood[key].makespan)].arc
            self.best_solution = neighborhood[min(neighborhood, key=lambda key: neighborhood[key].makespan)].schedule
            self.tabu_list.append(set([tabu_arc['i'], tabu_arc['j']]))
            self.tabu_list = self.tabu_list[-self.tabu_list_length:]
        return self.best_solution