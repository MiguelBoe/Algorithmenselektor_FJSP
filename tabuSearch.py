import copy
from neighborHood import NeighborHood
import plotly.figure_factory as ff
from utils import get_schedule_list
from critical_path import get_critical_path

class TabuSearch:
    def __init__(self, current_solution, max_iter, tabu_list_length):
        self.current_solution = copy.deepcopy(current_solution)
        self.best_solutions = {}
        self.critical_path = get_critical_path(self.current_solution)
        self.tabu_list_length = tabu_list_length
        self.max_iter = max_iter
        self.tabu_list = []

    def solve(self):
        for i in range(self.max_iter):
            neighborhood = NeighborHood(init_solution = self.current_solution, critical_path = get_critical_path(self.current_solution), tabu_list = self.tabu_list).get_neighborhood()
            tabu_arc = neighborhood[min(neighborhood, key=lambda key: neighborhood[key].makespan)].arc
            self.current_solution = neighborhood[min(neighborhood, key=lambda key: neighborhood[key].makespan)].schedule
            self.best_solutions.update({i:neighborhood[min(neighborhood, key=lambda key: neighborhood[key].makespan)]})
            self.tabu_list.append([tabu_arc[0], tabu_arc[1]])
            self.tabu_list = self.tabu_list[-self.tabu_list_length:]
        return self.best_solutions[min(self.best_solutions, key=lambda key: self.best_solutions[key].makespan)]