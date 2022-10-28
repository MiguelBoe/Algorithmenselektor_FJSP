import random
from random import randrange
import plotly.figure_factory as ff

def job_generator(max_job_count, max_task_count, max_processing_time):

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

def visualize_schedule(assigned_jobs, all_machines, plan_date):
    schedule_dict = []
    for machine in all_machines:
        assigned_jobs[machine].sort()
        for assigned_task in assigned_jobs[machine]:
            name = 'Job_%i' % assigned_task.job
            temp = dict(Task = machine,Start = plan_date + assigned_task.start,
                        Finish = plan_date + assigned_task.start + assigned_task.duration,
                        Resource = name)
            schedule_dict.append(temp)
    schedule_dict.sort(key = lambda x: x['Task'])
    return schedule_dict