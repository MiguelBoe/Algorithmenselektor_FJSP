import pandas as pd

jobs_data = [  # task = (machine_id, processing_time).
    [(0, 3), (1, 2), (2, 2)],  # Job0
    [(0, 2), (2, 1), (1, 5)],  # Job1
    [(0, 2), (1, 6), (2, 3)]  # Job2
]

def meta(jobs_data):

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
        temp = []
        for job in range(min(tasks, key=lambda x:x[0])[0], max(tasks, key=lambda x:x[0])[0]+1):
            filtered_list = [tup for tup in tasks if tup[0] == job]
            filtered_list2 = [tup for tup in filtered_list if tup[1] == min(filtered_list, key=lambda x:x[1])[1]]
            temp.append(filtered_list2[0])

        zz = {k: v for k, v in enumerate([x[3] for x in temp])}
        zz = {**z, **zz}
        zzt = [k for k in zz if zz[k] == min(zz.values())]

        filtered_list3 = [tup for tup in temp if tup[0] in min_keys]

        rr = {k: v for k, v in enumerate([x[3] for x in filtered_list3])}
        rr = {**r, **rr}
        rrt = max(rr, key=rr.get)





        schedule.append(filtered_list3[0])
        tasks = list(set(tasks).difference(set(filtered_list3)))
        zr = max(z[filtered_list3[0][2]]+filtered_list3[0][3], r[filtered_list3[0][0]]+filtered_list3[0][3])
        z.update({filtered_list3[0][2]:zr})
        r.update({filtered_list3[0][0]:zr})

        print()









    print()


meta(jobs_data)