import random
from random import randrange
from scheduling_ortools import *

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
            task_data.append((machine_id, randrange(max_processing_time)))
        jobs_data.append(task_data)

    return jobs_data

jobs_data = job_generator()

ortools_scheduler(jobs_data)