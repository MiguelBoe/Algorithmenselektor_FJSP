from dataclasses import dataclass, field
from typing import Tuple
from jobList import JobList
import plotly.figure_factory as ff


@dataclass
class Task:
    machine_id: int
    job_id: int
    duration: int
    task_id: int


@dataclass
class ScheduledTask(Task):
    start: int
    end: int
    task_on_machine_idx: int
    saz: int = field(init=False, default=0)
    sez: int = field(init=False, default=0)


def giffler_thompson(jobs_data: JobList) -> list[ScheduledTask]:
    """
    Berechnung eines Schedules mittels des Giffler und Thompson Algorithmus
    """

    schedule = []
    # dict_list = []

    # Liste der Tasksindizes welche nach Vorrangsbeziehungen zu Beginn verfügbar sind
    accessable_tasks_idx = [0] * len(jobs_data)

    # Liste der Zeitpunkte zu denen die Maschinen verfügbar sind
    num_machines = jobs_data.get_num_machines()
    access_time_machines = [0] * num_machines

    # Liste der Zeitpunkte zu denen der zuweisbare Task der Jobs weiterbearbeitet werden kann
    access_time_job = [0] * len(jobs_data)

    # Liste, die die Länge(Menge der Tasks) jedes Jobs enthält
    job_length = jobs_data.get_job_length()

    # Liste für kritischen Pfad beinhaltet wie viele tasks gerade auf der maschine sind
    num_tasks_per_machine = [0] * num_machines

    # Solange irgendein Eintrag der Liste job_length ungleich des Eintrags an der gleichen Stelle in accessable_tasks_idx ist, sind noch nicht alle Tasks eingeplant
    while any(
        job_len != acc_idx for job_len, acc_idx in zip(job_length, accessable_tasks_idx)
    ):

        # Initialisieren der Liste der zuweisbaren Tasks
        accessable_tasks = get_accessable_tasks(accessable_tasks_idx, jobs_data)

        # Auswahl des Tasks, der nach Giffler und Thompson als nächstes zugewiesen werden soll
        selected_task = choose_task(
            accessable_tasks, access_time_machines, access_time_job
        )

        # Kontrollieren ob mehr Tasks auf der gewählten Machine zuweisbar sind, als den ausgewählten Task
        task_on_machine = get_machine_tasks(
            task_list=accessable_tasks, machine_id=selected_task.machine_id
        )

        # Wenn es mehr als einen zuweisbaren Job auf der ausgewählten Maschine gibt
        if len(task_on_machine) > 1:
            # Auswahl des Tasks, der nach ausgewählter Prio-Regel als erstes dran ist
            selected_task = get_prio_task_LPT(task_on_machine, jobs_data)

        # Berechnung des Start- und Endwertes des ausgewählten Tasks
        start = max(
            access_time_machines[selected_task.machine_id],
            access_time_job[selected_task.job_id],
        )
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
        )

        # # scheduled_task zusätzlich als dict abspeichern
        # schedule_dict = dict(
        #     Task=f"Machine: {scheduled_task.machine_id}",
        #     Start=scheduled_task.start,
        #     Finish=scheduled_task.end,
        #     Job=scheduled_task.job_id,
        #     Resource=f"Task {scheduled_task.task_id} from job {scheduled_task.job_id}",
        # )

        # # Den einzuplanenden Task dem Schedule hinzufügen (dict)
        # dict_list.append(schedule_dict)

        # Den einzuplanenden Task dem Schedule hinzufügen
        schedule.append(scheduled_task)

        # print(f"Scheduled Task: {scheduled_task}")

        # Aktualisierung
        num_tasks_per_machine[selected_task.machine_id] += 1

        # Aktualisierung der aufgebrauchten Zeit an der Maschine und der Verfügbarkeit des Jobs
        access_time_job, access_time_machines = update_access_times(
            selected_task, access_time_machines, access_time_job
        )

        # Aktualisierung der zuweisbaren Tasks
        accessable_tasks_idx[selected_task.job_id] += 1

    return schedule


def update_access_times(
    selected_task: Task, access_time_machines: list, access_time_job: list
) -> Tuple[list, list]:
    """ Aktualisieren der Zugangszeit der ausgewählten Maschine und des Jobs dessen Task zugewiesen wurde."""

    machine = selected_task.machine_id
    job = selected_task.job_id

    # Neue Zeit entspricht der Taskdauer + max( Maschinenzugangszeit, Jobzugangszeit)
    new_accesstime = selected_task.duration + max(
        access_time_machines[machine], access_time_job[job]
    )

    access_time_machines[machine] = new_accesstime
    access_time_job[job] = new_accesstime

    return access_time_job, access_time_machines


def choose_task(
    accessable_tasks: list[Task], access_time_machines: list, access_time_job: list
) -> Task:
    """Auswahl der Maschine und des Tasks, der auf diese zugewiesen wird. """

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

    return accessable_tasks[selected_task_idx]


def get_accessable_tasks(accessable_tasks_idx: list, jobs_data: JobList) -> list[Task]:
    """ Rausschrieben der zuweisbaren Tasks mit Hilfe der Indizes. """
    accessable_tasks = []

    for job_id, (job, idx) in enumerate(
        zip(jobs_data.list_of_jobs, accessable_tasks_idx)
    ):
        if idx in range(len(job)):
            task = Task(
                machine_id=job[idx][0], duration=job[idx][1], job_id=job_id, task_id=idx
            )
            accessable_tasks.append(task)
    return accessable_tasks


def get_machine_tasks(task_list: list[Task], machine_id: int) -> list[Task]:
    """ Überprüfen ob auf der ausgewählten Maschine mehrere zuweisbare Tasks sind."""
    return [task for task in task_list if task.machine_id == machine_id]


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


#### Daten zum Testen aus Ablaufplanung (F. Jaehn, E. Pesch)
# jobs_data = [
#     [(0, 5), (1, 3), (2, 3), (3, 2)],
#     [(1, 4), (0, 7), (2, 8), (3, 6)],
#     [(3, 3), (2, 5), (1, 6), (0, 1)],
#     [(2, 4), (3, 7), (1, 1), (0, 2)],
# ]

# jobs_data = [
#     [(0, 2), (1, 3), (2, 8)],
#     [(0, 4), (1, 5), (2, 3)],
#     [(0, 2), (1, 4), (2, 5)],
#     [(0, 6), (1, 5), (2, 3)],
# ]

# #jobs_data = [
#     [(0, 2), (1, 3), (2, 8)],
#     [(2, 3), (0, 4), (1, 5)],
#     [(1, 4), (0, 2), (2, 5)],
#     [(2, 3), (1, 5), (0, 6) ],
# ]

# jobs_data = JobList(jobs_data)

# (schedule, dict_list,) = giffler_thompson(jobs_data)
