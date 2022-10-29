from utils import *
from scheduling_ortools import *
from scheduling_metaheuristic import *

#Config
solver = 'meta' # google, meta
max_job_count = 5
max_task_count = 5
max_processing_time = 5

#Job Generator
jobs_data = job_generator(max_job_count, max_task_count, max_processing_time)
jobs_data = [  # task = (machine_id, processing_time).
    [(0, 5), (1, 3), (2, 3), (3, 2)],  # Job0
    [(1, 4), (0, 7), (2, 8), (3, 6)],  # Job1
    [(3, 3), (2, 5), (1, 6), (0, 1)],  # Job2
    [(2, 4), (3, 7), (1, 1), (0, 2)]  # Job2
]

#Selection of the solver
if solver == 'google':
    assigned_jobs, all_machines = ortools_scheduler(jobs_data)
    schedule_dict = visualize_schedule(assigned_jobs=assigned_jobs, all_machines=all_machines, plan_date=0)
elif solver == 'meta':
    schedule_dict = metaheuristic(jobs_data)

#Visualization
fig = ff.create_gantt(schedule_dict, index_col='Resource', show_colorbar=True, group_tasks=True)
fig.layout.xaxis.type = 'linear'
fig.show()

print('Hallo')