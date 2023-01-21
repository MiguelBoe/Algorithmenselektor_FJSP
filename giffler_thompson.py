from dataclasses import dataclass, field
from typing import Tuple, List
from jobList import JobList
import numpy as np
from operator import attrgetter

@dataclass
class Task:
    machine_id: int
    job_id: int
    duration: int
    task_id: int


@dataclass
class ScheduledTask(Task):
    start: int = field(default=0)
    end: int = field(default=0)
    task_on_machine_idx: int = field(default=0)
    longest_path: int = field(init=False, default=0)
    pred: List = field(default_factory=lambda: [])


def giffler_thompson(jobs_data: JobList, priority_rule) -> list[ScheduledTask]:
    """
    Berechnung eines Schedules mittels des Giffler und Thompson Algorithmus
    """

    schedule = {}

    # Liste der Tasksindizes welche nach Vorrangsbeziehungen zu Beginn verfügbar sind
    accessable_tasks_idx = [0] * len(jobs_data)

    # Liste der Zeitpunkte zu denen die Maschinen verfügbar sind (Anfangs Zeitpunkt 0)
    num_machines = jobs_data.get_num_machines()
    access_time_machines = [0] * num_machines

    # Liste der Zeitpunkte zu denen der zuweisbare Task der Jobs weiterbearbeitet werden kann (Anfangs Zeitpunkt 0)
    access_time_job = [0] * len(jobs_data)

    # Liste, die die Länge(Menge der Tasks) jedes Jobs enthält
    job_length = jobs_data.get_job_length()

    # Liste für kritischen Pfad beinhaltet wie viele tasks gerade auf der maschine sind
    num_tasks_per_machine = [0] * num_machines

    # Solange irgendein Eintrag der Liste job_length ungleich des Eintrags an der gleichen Stelle in accessable_tasks_idx ist, sind noch nicht alle Tasks eingeplant
    idx_task_in_schedule = 0  # ????
    while any(job_len != acc_idx for job_len, acc_idx in zip(job_length, accessable_tasks_idx)):

        # Initialisieren der Liste der zuweisbaren Tasks
        accessable_tasks = get_accessable_tasks(accessable_tasks_idx, jobs_data)

        # Auswahl des Tasks, der nach Giffler und Thompson als nächstes zugewiesen werden soll
        selected_task, min_value = choose_task(accessable_tasks, access_time_machines, access_time_job)

        # Kontrollieren ob mehr Tasks auf der gewählten Machine zuweisbar sind, als den ausgewählten Task
        available_tasks_on_machine = get_machine_tasks(
            task_list=accessable_tasks,
            machine_id=selected_task.machine_id,
            access_time_job=access_time_job,
            min_value=min_value,
        )

        # Wenn es mehr als einen zuweisbaren Job auf der ausgewählten Maschine gibt
        if len(available_tasks_on_machine) > 1:
            # Auswahl des Tasks, der nach ausgewählter Prio-Regel als erstes dran ist
            if priority_rule == "LPT":
                selected_task = get_prio_task_LPT(available_tasks_on_machine, jobs_data)
            elif priority_rule == "SPT":
                selected_task = get_prio_task_SPT(available_tasks_on_machine, jobs_data)
            elif priority_rule == "LRPT" or "SRPT":
                selected_task = get_prio_task_RPT(available_tasks_on_machine, jobs_data, priority_rule)

        # Berechnung des Start- und Endwertes des ausgewählten Tasks
        start = max(access_time_machines[selected_task.machine_id], access_time_job[selected_task.job_id])
        end = start + selected_task.duration

        # Den ausgewählten Task in die dataclass ScheduledTask aufnehmen und um start und end erweitern
        scheduled_task = ScheduledTask(
            machine_id=selected_task.machine_id,
            job_id=selected_task.job_id,
            duration=selected_task.duration,
            task_id=selected_task.task_id,
            start=start,
            end=end,
            task_on_machine_idx=num_tasks_per_machine[selected_task.machine_id],
            pred=get_predecessor(
                schedule=schedule,
                task_id=selected_task.task_id,
                task_on_machine_idx=num_tasks_per_machine[selected_task.machine_id],
                machine_id=selected_task.machine_id,
                job_id=selected_task.job_id,
            ),
        )

        # Den einzuplanenden Task dem Schedule hinzufügen
        schedule[idx_task_in_schedule] = scheduled_task
        idx_task_in_schedule += 1

        # Aktualisierung
        num_tasks_per_machine[selected_task.machine_id] += 1

        # Aktualisierung der aufgebrauchten Zeit an der Maschine und der Verfügbarkeit des Jobs
        access_time_job, access_time_machines = update_access_times(
            selected_task, access_time_machines, access_time_job
        )

        # Aktualisierung der zuweisbaren Tasks
        accessable_tasks_idx[selected_task.job_id] += 1

    print(f"\nInitial solution found with a makespan of {end}")

    return schedule


def update_access_times(
    selected_task: Task, access_time_machines: list, access_time_job: list) -> Tuple[list, list]:

    """ Aktualisieren der Zugangszeit der ausgewählten Maschine und des Jobs dessen Task zugewiesen wurde."""

    machine = selected_task.machine_id
    job = selected_task.job_id

    # Neue Zeit entspricht der Taskdauer + max(Maschinenzugangszeit, Jobzugangszeit)

    new_accesstime = selected_task.duration + max(access_time_machines[machine], access_time_job[job])

    access_time_machines[machine] = new_accesstime
    access_time_job[job] = new_accesstime

    return access_time_job, access_time_machines



def choose_task(accessable_tasks: list[Task], access_time_machines: list, access_time_job: list) -> Task:

    """Auswahl der Maschine und des Tasks, der auf diese zugewiesen wird."""

    criteria = []

    for task in accessable_tasks:
        machine = task.machine_id
        job_id = task.job_id

        # Berechnung des Kriteriums nach Giffler und Thompson
        c = task.duration + max(access_time_machines[machine], access_time_job[job_id])
        criteria.append(c)

    # Auswahl des minimalen Wertes
    min_value = min(criteria)
    # Auswahl des Tasks, bei dem der Wert am geringsten ist
    selected_task_idx = criteria.index(min_value)

    return accessable_tasks[selected_task_idx], min_value


def get_accessable_tasks(accessable_tasks_idx: list, jobs_data: JobList) -> list[Task]:
    """ Rausschrieben der zuweisbaren Tasks mit Hilfe der Indizes. """
    accessable_tasks = []


    for job_id, (job, idx) in enumerate(zip(jobs_data.list_of_jobs, accessable_tasks_idx)):
        if idx in range(len(job)):
            task = Task(machine_id=job[idx][0], duration=job[idx][1], job_id=job_id, task_id=idx)
            accessable_tasks.append(task)
    return accessable_tasks


def get_machine_tasks(task_list: list[Task], machine_id: int, access_time_job: list, min_value: int) -> list[Task]:
    """ Überprüfen ob auf der ausgewählten Maschine mehrere zuweisbare Tasks sind."""
    tasks_on_machine = [task for task in task_list if task.machine_id == machine_id]
    available_tasks_on_machine = []
    for task in tasks_on_machine:
        end_time_job = access_time_job[task.job_id]
        if end_time_job < min_value:
            available_tasks_on_machine.append(task)
    return available_tasks_on_machine

def get_prio_task_LPT(task_on_machine: list[Task], jobs_data: JobList) -> Task:
    """ Wenn mehr als ein Task zuweisbar ist soll anhand der LPT regel der Task bestimmt werden, welcher zuerst eingeplant wird."""
    # Berechnen der Jobdauer aller jobs
    jobs_duration = jobs_data.get_processing_time()  # list[int]
    # Gleich 0 für LPT
    job_duration = 0
    # Kontrolle für jeden zur auswahl stehenden Task ob die Dauer des zugehörigen Jobs länger ist als die des Vorgängers
    for task in task_on_machine:
        if jobs_duration[task.job_id] > job_duration:
            job_duration = jobs_duration[task.job_id]
            selected_task = task
    return selected_task


def get_prio_task_SPT(task_on_machine: list[Task], jobs_data: JobList) -> Task:
    """ Wenn mehr als ein Task zuweisbar ist soll anhand der LPT regel der Task bestimmt werden, welcher zuerst eingeplant wird."""
    jobs_duration = jobs_data.get_processing_time()  # [durations]
    # Große Zahl für SPT
    job_duration = 1e6
    # Kontrolle für jeden zur auswahl stehenden Task ob die Dauer des zugehörigen Jobs kürzer ist als die des Vorgängers
    for task in task_on_machine:
        if jobs_duration[task.job_id] < job_duration:
            job_duration = jobs_duration[task.job_id]
            selected_task = task
    return selected_task


def get_prio_task_RPT(task_on_machine: list[Task], jobs_data: JobList, priority_rule) -> Task:
    job_ids = [o.job_id for o in task_on_machine]
    task_ids = [o.task_id for o in task_on_machine]

    remaining_processing_time = {}
    index=0
    for x, y in zip(job_ids, task_ids):
        remaining_processing_time.update({index:sum(task[1] for task in jobs_data.list_of_jobs[x][y:]) for job in job_ids})
        index += 1

    if priority_rule == 'LRPT':
        selected_task = task_on_machine[max(remaining_processing_time, key=remaining_processing_time.get)]
    elif priority_rule == 'SRPT':
        selected_task = task_on_machine[min(remaining_processing_time, key=remaining_processing_time.get)]

    return selected_task


# Mit Hilfe dieser Funktion werden während der Generierung der Startlösung die Vorgänger-Operationen abgespeichert.
def get_predecessor(schedule,task_id, task_on_machine_idx, machine_id, job_id):
    return [k for k, v in schedule.items() if (v.job_id == job_id and v.task_id ==task_id-1) or
            (v.machine_id==machine_id and v.task_on_machine_idx==task_on_machine_idx-1)]