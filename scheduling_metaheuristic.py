from collections import Counter
from criticalpath import Node

def giffler_thompson(jobs_data):

    all_machines = set(list(task[0] for job in jobs_data for task in job))
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
        for job in list({k: v for k, v in enumerate([x[0] for x in tasks])}.values()):
            actual_jobs = [tup for tup in tasks if tup[0] == job]
            actual_jobs = [tup for tup in actual_jobs if tup[1] == min(actual_jobs, key=lambda x:x[1])[1]]
            temp_jobs.update({job:actual_jobs})

        temp_z,temp_duration,temp_decision_maker = {},{},{}
        for job in list({k: v for k, v in enumerate([x[0] for x in tasks])}.values()):
            temp_z.update({job:z[temp_jobs[job][-1][-2]]})
            temp_duration.update({job:temp_jobs[job][-1][-1]})
            temp_decision_maker.update({job:max(temp_z[job], r[job])})

        temp_decision_maker = dict(Counter(temp_duration)+Counter(temp_decision_maker))
        jobs_for_schedule = [k for k in temp_decision_maker if temp_decision_maker[k] == min(temp_decision_maker.values())]

        if len(jobs_for_schedule)>1:
            machine_finder = {k: v for k, v in temp_jobs.items() if v[-1][-2] == temp_jobs[jobs_for_schedule[0]][-1][-2]}
            scheduled_job = min(machine_finder.items(), key=lambda i : i[1][-1][-1])[0]
        else:
            scheduled_job = jobs_for_schedule[0]

        scheduled_job_complete = temp_jobs[scheduled_job][0] + (max(temp_z[scheduled_job], r[scheduled_job]),)
        schedule.append(scheduled_job_complete)
        tasks = set(tasks).difference(set(temp_jobs[scheduled_job]))
        makespan = max((r[temp_jobs[scheduled_job][-1][0]] + temp_jobs[scheduled_job][-1][-1]),(temp_z[scheduled_job] + temp_jobs[scheduled_job][-1][-1]))
        r.update({scheduled_job: makespan})
        z.update({temp_jobs[scheduled_job][-1][-2]: makespan})

    print(f'\nSolution found with a makespan of {makespan}')

    schedule_list = []
    schedule_dict = {}
    for i in range(len(schedule)):
        schedule_dict.update({i:{'Task': schedule[i][2],
                              'Start': schedule[i][4],
                              'Finish': schedule[i][4] + schedule[i][3],
                              'Resource': f'Job_{schedule[i][0]}'}})

        schedule_list.append({'Task': schedule[i][2],
                              'Start': schedule[i][4],
                              'Finish': schedule[i][4] + schedule[i][3],
                              'Resource': f'Job_{schedule[i][0]}'})

    return schedule_list, schedule_dict

#Get Parents
def get_parents(schedule_dict):
    for key, value in schedule_dict.items():
        value.update({'Duration': value['Finish']-value['Start'],'Predecessor':list({k: v for k, v in schedule_dict.items() if v['Finish'] == value['Start'] and
                                               (v['Task'] == value['Task'] or v['Resource'] == value['Resource'])})})
    return schedule_dict

#Critical Path
def get_critical_path(schedule_dict):

    nodes = {}
    p = Node('project')

    for node in schedule_dict.keys():
        nodes.update({f'node_{node}':p.add(Node(f'{node}', duration=schedule_dict[node]['Duration'], lag=0))})
    for k in nodes.keys():
        for i in schedule_dict[int(k.split("_",1)[1])]['Predecessor']:
            print(nodes[k], nodes[f'node_{i}'])
            p.link(nodes[k], nodes[f'node_{i}'])

    p.update_all()
    critical_path = p.get_critical_path()

    return critical_path