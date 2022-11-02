from collections import Counter
import plotly.figure_factory as ff

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

    schedule_dict = []
    for i in range(len(schedule)):
        schedule_dict.append({'Task': schedule[i][2],
                              'Start': schedule[i][4],
                              'Finish': schedule[i][4] + schedule[i][3],
                              'Resource': f'Job_{schedule[i][0]}'})

    return schedule_dict


class TabuSearch:
    def __init__(self, schedule_dict):
        self.currSolution = schedule_dict

    def get_critical_path(self, critical_path, last_job):
        #critical_path_0 = []
        #last_job = max(self.currSolution, key=lambda x: x['Finish'])
        critical_path.append(last_job)

        while last_job['Start'] != 0:
            actual_job = list(filter(lambda v: v['Finish'] == last_job['Start'] and
                                               (v['Task'] == last_job['Task'] or
                                                v['Resource'] == last_job['Resource']), self.currSolution))
            # if len(actual_job) == 1:
            critical_path.append(actual_job[0])
            last_job = actual_job[0]
            # else:
            #     for job in range(len(actual_job)):
            #         globals()[f'critical_path_{job+1}'] = TabuSearch.get_critical_path(self, critical_path = critical_path, last_job = actual_job[job])

        print()