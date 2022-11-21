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
import time
import copy


# Config
max_job_count = 10
max_machine_count = 10
max_duration = 10
instances_count = 10
solver = "meta"  # google, meta
max_iter = 50
tabu_list_length = 5
time_limit_in_seconds = 1


# Job Generator
data = job_generator(max_job_count, max_machine_count, max_duration, instances_count)
data = [  # task = (machine_id, processing_time).
    [(0, 5), (1, 3), (2, 3), (3, 2)],  # Job0
    [(1, 4), (0, 7), (2, 8), (3, 6)],  # Job1
    [(3, 3), (2, 5), (1, 6), (0, 1)],  # Job2
    [(2, 4), (3, 7), (1, 1), (0, 2)],  # Job2
]

# Selection of the solver
if solver == "google":
    assigned_jobs, all_machines = ortools_scheduler(data=data, time_limit_in_seconds=time_limit_in_seconds)
    schedule_list = visualize_schedule(assigned_jobs=assigned_jobs, all_machines=all_machines, plan_date=0)
elif solver == "meta":
    data = JobList(data)
    init_schedule = giffler_thompson(data)
    best_solution = TabuSearch(current_solution=init_schedule, max_iter=max_iter, tabu_list_length=tabu_list_length, time_limit_in_seconds=time_limit_in_seconds).solve()
    schedule_list = get_schedule_list(best_solution.schedule)
    print(f'\nBest solution with TabuSearch found with a makespan of {best_solution.makespan}')

# Visualization
fig = ff.create_gantt(schedule_list, index_col="Resource", show_colorbar=True, group_tasks=True)
fig.layout.xaxis.type = "linear"
fig.show()