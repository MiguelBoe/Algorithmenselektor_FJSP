import pandas as pd
from collections import Counter

jobs_data = [  # task = (machine_id, processing_time).
    [(0, 5), (1, 3), (2, 3), (3, 2)],  # Job0
    [(1, 4), (0, 7), (2, 8), (3, 6)],  # Job1
    [(3, 3), (2, 5), (1, 6), (0, 1)],  # Job2
    [(2, 4), (3, 7), (1, 1), (0, 2)]  # Job2
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


        kk,zz,rrt = {},{},{}
        for job in list(set({k: v for k, v in enumerate([x[0] for x in tasks])}.values())):
            kk.update({job:z[tuple(temp[job])[-1][-2]]})
            zz.update({job:tuple(temp[job])[-1][-1]})
            rrt.update({job:max(kk[job], r[job])})




        gg = dict(Counter(zz)+Counter(rrt))
        zzt = [k for k in gg if gg[k] == min(gg.values())]

        if len(zzt)>1:
            test = {k: v for k, v in temp.items() if tuple(v)[-1][-2] == tuple(temp[zzt[0]])[-1][-2]}
            ho = max(test.items(), key=lambda i : tuple(i[1])[-1][-1])[0]
        else:
            ho = zzt[0]

        schedule.append(temp[ho])
        tasks = list(set(tasks).difference(set(temp[ho])))
        print(ho)
        zr = max((r[tuple(temp[ho])[-1][0]] + tuple(temp[ho])[-1][-1]), (kk[ho]+tuple(temp[ho])[-1][-1]))
        r.update({ho: zr})
        z.update({tuple(temp[ho])[-1][-2]: zr})






    print()


meta(jobs_data)