import pandas as pd

jobs_data = [  # task = (machine_id, processing_time).
    [(0, 3), (1, 2), (2, 2)],  # Job0
    [(0, 2), (2, 1), (1, 5)],  # Job1
    [(0, 1), (1, 6), (2, 3)]  # Job2
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
        temp = {}
        for job in list(set({k: v for k, v in enumerate([x[0] for x in tasks])}.values())):
            filtered_list = [tup for tup in tasks if tup[0] == job]
            filtered_list2 = [tup for tup in filtered_list if tup[1] == min(filtered_list, key=lambda x:x[1])[1]]
            temp.update({job:tuple(filtered_list2)})

        kk,zz = {},{}
        for job in list(set({k: v for k, v in enumerate([x[0] for x in tasks])}.values())):
            kk.update({job:z[tuple(temp[job])[-1][-2]]})
            zz.update({job:tuple(temp[job])[-1][-1]})


        rr = {**r, **zz}
        zzt = [k for k in zz if zz[k] == min(zz.values())]



        if len(zzt)<2:
            schedule.append(temp[zzt[0]])
            tasks = list(set(tasks).difference(set(temp[zzt[0]])))
            print(zzt[0])
            zr = max((r[tuple(temp[zzt[0]])[-1][0]] + tuple(temp[zzt[0]])[-1][-1]), (kk[zzt[0]]+tuple(temp[zzt[0]])[-1][-1]))
            r.update({zzt[0]: zr})
            z.update({tuple(temp[zzt[0]])[-1][-2]: zr})


    print()


meta(jobs_data)