from job_list import JobList
from scheduling_giffler_thompson import ScheduledTask, giffler_thompson


def main():
    #### Daten zum Testen aus Ablaufplanung (F. Jaehn, E. Pesch)
    jobs_data = [
        [(0, 5), (1, 3), (2, 3), (3, 2)],
        [(1, 4), (0, 7), (2, 8), (3, 6)],
        [(3, 3), (2, 5), (1, 6), (0, 1)],
        [(2, 4), (3, 7), (1, 1), (0, 2)],
    ]

    jobs_data = JobList(jobs_data)

    schedule, schedule_list = giffler_thompson(jobs_data)

    get_saz_sez(schedule)

    critical_path = get_critical_path(schedule)

    print(critical_path)


def get_critical_path(schedule):
    return [task for task in schedule if task.start == task.saz]

def get_saz_sez(schedule: list[ScheduledTask]):
    schedule[-1].saz = schedule[-1].start
    schedule[-1].sez = schedule[-1].end

    # Frühester Anfangs und Endzeitpunkt
    for task in reversed(schedule[:-1]):
        # finde Nachfolgertasks nachfolger im job und nachfolger auf maschine
        successor_job = None
        successor_machine = None

        for task2 in reversed(schedule):
            if task2.machine_id == task.machine_id and task2.task_on_machine_idx == (
                task.task_on_machine_idx + 1
            ):
                successor_machine = task2
            if task2.job_id == task.job_id and task2.task_id == (task.task_id + 1):
                successor_job = task2

        if successor_job is None and successor_machine is None:
            task.sez = schedule[-1].sez

        elif successor_job is None:
            successor_machine_saz = successor_machine.saz

            task.sez = successor_machine_saz

        elif successor_machine is None:
            successor_job_saz = successor_job.saz

            task.sez = successor_job_saz

        else:
            successor_machine_saz = successor_machine.saz
            successor_job_saz = successor_job.saz

            task.sez = min(successor_machine_saz, successor_job_saz)

        task.saz = task.sez - task.duration


if __name__ == "__main__":
    main()