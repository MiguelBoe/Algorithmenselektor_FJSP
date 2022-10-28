import pandas as pd
from collections import Counter

jobs_data = [  # task = (machine_id, processing_time).
    [(0, 5), (1, 3), (2, 3), (3, 2)],  # Job0
    [(1, 4), (0, 7), (2, 8), (3, 6)],  # Job1
    [(3, 3), (2, 5), (1, 6), (0, 1)],  # Job2
    [(2, 4), (3, 7), (1, 1), (0, 2)]  # Job2
]

def metaheuristic(jobs_data):

    all_machines = list(set(list(task[0] for job in jobs_data for task in job)))
    machines_count = len(all_machines)

    z = {}
    for machine in all_machines:
        z.update({machine:0})

    r = {}
    for job in range(len(jobs_data)):
        r.update({job: 0})

    tasks = []
    for job_id, job in enumerate(jobs_data):
        for task_id, task in enumerate(job):
            duration = task[1]
            machine = task[0]
            tasks.append((job_id, task_id, machine, duration))

    schedule = []
    for task in range(len(tasks)):
        temp_jobs = {}
        for job in list(set({k: v for k, v in enumerate([x[0] for x in tasks])}.values())):
            actual_jobs = [tup for tup in tasks if tup[0] == job]
            actual_jobs = [tup for tup in actual_jobs if tup[1] == min(actual_jobs, key=lambda x:x[1])[1]]
            temp_jobs.update({job:tuple(actual_jobs)})

        temp_z,temp_duration,temp_decision_maker = {},{},{}
        for job in list(set({k: v for k, v in enumerate([x[0] for x in tasks])}.values())):
            temp_z.update({job:z[tuple(temp_jobs[job])[-1][-2]]})
            temp_duration.update({job:tuple(temp_jobs[job])[-1][-1]})
            temp_decision_maker.update({job:max(temp_z[job], r[job])})

        temp_decision_maker = dict(Counter(temp_duration)+Counter(temp_decision_maker))
        jobs_for_schedule = [k for k in temp_decision_maker if temp_decision_maker[k] == min(temp_decision_maker.values())]

        if len(jobs_for_schedule)>1:
            machine_finder = {k: v for k, v in temp_jobs.items() if tuple(v)[-1][-2] == tuple(temp_jobs[jobs_for_schedule[0]])[-1][-2]}
            scheduled_job = max(machine_finder.items(), key=lambda i : tuple(i[1])[-1][-1])[0]
        else:
            scheduled_job = jobs_for_schedule[0]

        schedule.append(temp_jobs[scheduled_job])
        tasks = list(set(tasks).difference(set(temp_jobs[scheduled_job])))
        makespan = max((r[tuple(temp_jobs[scheduled_job])[-1][0]] + tuple(temp_jobs[scheduled_job])[-1][-1]), (temp_z[scheduled_job]+tuple(temp_jobs[scheduled_job])[-1][-1]))
        r.update({scheduled_job: makespan})
        z.update({tuple(temp_jobs[scheduled_job])[-1][-2]: makespan})
    print(f'\nSolution found with a makespan of {makespan}')
metaheuristic(jobs_data)