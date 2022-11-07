import random
from random import randrange
import pickle
from job_list import JobList


def job_generator(max_job_count, max_machine_count, max_duration):

    data = []

    for _ in range(10):

        # Anzahl der Jobs
        num_jobs = random.randint(2, max_job_count)

        # Anzahl der Maschinen
        num_machines = random.randint(2, max_machine_count)

        jobs_data = JobList.create(max_duration, num_machines, num_jobs)

        data.append(jobs_data)

    # speichern der Datei
    # with open("job_data.pkl", "wb") as out_file:
    #     pickle.dump(data, out_file)
    #
    # # lesen der Datei
    # with open("job_data.pkl", "rb") as in_file:
    #     data = pickle.load(in_file)

    return data

def visualize_schedule(assigned_jobs, all_machines, plan_date):
    schedule_list = []
    for machine in all_machines:
        assigned_jobs[machine].sort()
        for assigned_task in assigned_jobs[machine]:
            name = 'Job_%i' % assigned_task.job
            temp = dict(Task = machine,Start = plan_date + assigned_task.start,
                        Finish = plan_date + assigned_task.start + assigned_task.duration,
                        Resource = name)
            schedule_list.append(temp)
    schedule_list.sort(key = lambda x: x['Task'])
    return schedule_list