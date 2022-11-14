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
import time

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
    schedule, schedule_list = giffler_thompson(data)
    critical_path = get_critical_path(schedule)
    print((time.time() - start_time))


    test1 = schedule[10]
    test2 = schedule[12]
    # test2.start = test1.start
    # test2.end = test2.start + test2.duration
    # test1.start = test2.end
    # test1.end = test1.start + test1.duration
    test2.task_on_machine_idx = 1
    test1.task_on_machine_idx = 2
    test1.pred = get_predecessor(schedule = schedule, task_id = test1.task_id, task_on_machine_idx = test1.task_on_machine_idx, machine_id = test1.machine_id, job_id = test1.job_id)
    test2.pred = get_predecessor(schedule=schedule, task_id=test2.task_id, task_on_machine_idx=test2.task_on_machine_idx, machine_id=test2.machine_id, job_id=test2.job_id)

    #for i in list(schedule.keys()):
    #    schedule[i].pred = get_predecessor(schedule=schedule, task_id=schedule[i].task_id, task_on_machine_idx=schedule[i].task_on_machine_idx, machine_id=schedule[i].machine_id, job_id=schedule[i].job_id)


    def get_earliest_start(schedule):
        for i in list(schedule.keys()):
            pred_start_times = [schedule[x].end for x in schedule[i].pred]
            pred_start_times.append(0)
            schedule[i].start = max(pred_start_times)
            schedule[i].end = schedule[i].start + schedule[i].duration


    get_earliest_start(schedule)

    testss = []
    for k,v in schedule.items():
        testss.append({'Task':v.machine_id, 'Start':v.start, 'Finish':v.end, 'Resource': f'Job_{v.job_id}'})



# Visualization
fig = ff.create_gantt(testss, index_col="Resource", show_colorbar=True, group_tasks=True)
fig.layout.xaxis.type = "linear"
fig.show()

print()