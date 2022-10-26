import random
from random import randrange
from scheduling_ortools import *
import plotly.figure_factory as ff

max_job_count = 10
max_task_count = 10
max_processing_time = 10

def job_generator():

    jobs_data = []
    job_count = randrange(2,max_job_count)
    for job in range(job_count):
        task_data = []
        task_count = randrange(2,max_task_count)
        machine_id_del = []
        for task in range(task_count):
            machine_id = random.choice(list(set(range(task_count)).difference(set(machine_id_del))))
            machine_id_del.append(machine_id)
            task_data.append((machine_id, randrange(1, max_processing_time)))
        jobs_data.append(task_data)

    return jobs_data

jobs_data = job_generator()
assigned_jobs, all_machines = ortools_scheduler(jobs_data)

#Visualisation function
def visualize_schedule(assigned_jobs, all_machines, plan_date):
    res = []
    for machine in all_machines:
        assigned_jobs[machine].sort()
        for assigned_task in assigned_jobs[machine]:
            name = 'Job_%i' % assigned_task.job
            temp = dict(Task = machine,Start = plan_date + assigned_task.start,
                        Finish = plan_date + assigned_task.start + assigned_task.duration,
                        Resource = name)
            res.append(temp)
    res.sort(key = lambda x: x['Task'])
    return res

res = visualize_schedule(assigned_jobs = assigned_jobs,all_machines = all_machines, plan_date = 0)
fig = ff.create_gantt(res, index_col = 'Resource', show_colorbar = True, group_tasks = True)
fig.layout.xaxis.type = 'linear'
fig.show()

print('Hallo')