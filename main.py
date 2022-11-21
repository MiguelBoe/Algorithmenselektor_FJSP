"""
@author: pretz & böttcher

#-----------------------------------------------------------------------------#
#         Projektseminar Business Analytics - Wintersemester 22/23            #
#-----------------------------------------------------------------------------#
#                                                                             #
#                                 Main File                                   #
#                                                                             #
#-----------------------------------------------------------------------------#
"""

from utils import *
from scheduling_ortools import *
from scheduling_giffler_thompson import giffler_thompson
import plotly.figure_factory as ff
from scheduling_giffler_thompson import get_predecessor
from tabuSearch import TabuSearch
import pickle
import time
import copy


# Konfigurationsbereich
#----------------------------------------------------------------------------------------------------------------------#
# Select solver and set time_limit
solver = 'meta'  # google, meta
time_limit_in_seconds = 1

# Config for TabuSearch
max_iter = 100
tabu_list_length = 1

# Data path
data_path = '\\Users\\migue\\PycharmProjects\\Algorithmenselektor_JSP\\data'
#----------------------------------------------------------------------------------------------------------------------#


# Load data
with open(f'{data_path}\\data.pkl', 'rb') as in_file:
    data = pickle.load(in_file)

# data = [  # task = (machine_id, processing_time).
#     [(0, 5), (1, 3), (2, 3), (3, 2)],  # Job0
#     [(1, 4), (0, 7), (2, 8), (3, 6)],  # Job1
#     [(3, 3), (2, 5), (1, 6), (0, 1)],  # Job2
#     [(2, 4), (3, 7), (1, 1), (0, 2)],  # Job2
# ]
# data = JobList(data)

# Selection of the solver
if solver == "google":
    assigned_jobs, all_machines = ortools_scheduler(data=data[0].list_of_jobs, time_limit_in_seconds=time_limit_in_seconds)
    schedule_list = visualize_schedule(assigned_jobs=assigned_jobs, all_machines=all_machines, plan_date=0)
elif solver == "meta":
    init_schedule = giffler_thompson(data[0])
    best_solution = TabuSearch(current_solution=init_schedule, max_iter=max_iter, tabu_list_length=tabu_list_length, time_limit_in_seconds=time_limit_in_seconds).solve()
    schedule_list = get_schedule_list(best_solution.schedule)
    print(f'\nBest solution with TabuSearch found with a makespan of {best_solution.makespan}')

# Visualization
fig = ff.create_gantt(schedule_list, index_col="Resource", show_colorbar=True, group_tasks=True)
fig.layout.xaxis.type = "linear"
fig.show()