import copy
from neighborHood import NeighborHood
import plotly.figure_factory as ff
from utils import get_schedule_list
from critical_path import get_critical_path

class TabuSearch:
    def __init__(self, current_solution, max_iter, tabu_list_length):
        self.best_solution = copy.deepcopy(current_solution)
        self.critical_path = get_critical_path(self.best_solution)
        self.max_iter = max_iter
        self.tabu_list = [0]*tabu_list_length

    def solve(self):
        for i in range(self.max_iter):
            neighborhood = NeighborHood(init_solution = self.best_solution, critical_path = get_critical_path(self.best_solution)).get_neighborhood()
            self.best_solution = neighborhood[min(neighborhood, key=lambda key: neighborhood[key].makespan)].schedule

        return self.best_solution