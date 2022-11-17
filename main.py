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
from critical_path import get_critical_path
from scheduling_giffler_thompson import get_predecessor
from neighborhood_old import *
import time
import copy
from neighborHood import NeighborHood

# Config
solver = "meta"  # google, meta
max_job_count = 10
max_machine_count = 10
max_duration = 10

# Job Generator
data = job_generator(max_job_count, max_machine_count, max_duration)
data = [  # task = (machine_id, processing_time).
    [(0, 5), (1, 3), (2, 3), (3, 2)],  # Job0
    [(1, 4), (0, 7), (2, 8), (3, 6)],  # Job1
    [(3, 3), (2, 5), (1, 6), (0, 1)],  # Job2
    [(2, 4), (3, 7), (1, 1), (0, 2)],  # Job2
]

# Selection of the solver
if solver == "google":
    assigned_jobs, all_machines = ortools_scheduler(data[0].list_of_jobs)
    schedule_list = visualize_schedule(assigned_jobs=assigned_jobs, all_machines=all_machines, plan_date=0)
elif solver == "meta":
    start_time = time.time()
    data = JobList(data)
    schedule = giffler_thompson(data)
    critical_path = get_critical_path(schedule)
    print((time.time() - start_time))

    neighborhood = NeighborHood(init_solution = schedule, critical_path = critical_path).get_neighborhood()
    schedule2 = neighborhood[0].schedule
    critical_path2 = get_critical_path(schedule2)
    neighborhood2 = NeighborHood(init_solution=schedule2, critical_path=critical_path2).get_neighborhood()



    schedule_list = get_schedule_list(neighborhood2[0].schedule)

# Visualization
fig = ff.create_gantt(schedule_list, index_col="Resource", show_colorbar=True, group_tasks=True)
fig.layout.xaxis.type = "linear"
fig.show()

print()