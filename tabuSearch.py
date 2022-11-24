from neighborHood import NeighborHood, NeighborhoodSolution
import plotly.figure_factory as ff
from utils import get_schedule_list
from critical_path import get_critical_path
import time

class TabuSearch:
    def __init__(self, current_solution, max_iter, tabu_list_length, time_limit_in_seconds):
        self.current_solution = current_solution
        self.best_solutions = {0:NeighborhoodSolution(schedule=current_solution, makespan=current_solution[max(current_solution, key=lambda key: current_solution[key].end)].end, arc=[])}
        self.critical_path = get_critical_path(self.current_solution)
        self.tabu_list_length = tabu_list_length
        self.max_iter = max_iter
        self.time_limit_in_seconds = time_limit_in_seconds
        self.tabu_list = []

    def solve(self):
        timeout = time.time() + self.time_limit_in_seconds
        for i in range(self.max_iter):
            neighborhood = NeighborHood(init_solution = self.current_solution, critical_path = get_critical_path(self.current_solution), tabu_list = self.tabu_list).get_neighborhood()
            if neighborhood and time.time() < timeout:
                new_solution = neighborhood[min(neighborhood, key=lambda key: neighborhood[key].makespan)]
                tabu_arc = new_solution.arc
                self.current_solution = new_solution.schedule
                self.best_solutions.update({i+1:new_solution})
                self.tabu_list.append([tabu_arc[0], tabu_arc[1]])
                self.tabu_list = self.tabu_list[-self.tabu_list_length:]
            else: break
        return self.best_solutions[min(self.best_solutions, key=lambda key: self.best_solutions[key].makespan)]