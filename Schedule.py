"""Class für Schedule"""

from jobList import JobList
from tasks import ScheduledTask


class Schedule:
    def __init__(self):

        # self.schedule = schedule

        self.task_dict = {}
        self.last_end_time: int = 0
        self.last_task: ScheduledTask = None

        # self.critical_path = self.get_critical_path()
        # self.neighborhood_n1 = self.get_neighborhood_n1()
        # self.neighborhood_n5 = self.get_neighborhood_n5()

    def add_task(self, task: ScheduledTask) -> None:
        if task.end > self.last_end_time:
            self.last_end_time = task.end
            self.last_task = task

        self.task_dict[task.id] = task

    def find_task(self, id: int) -> ScheduledTask:
        return self.task_dict[id]

    @property
    def makespan(self) -> int:
        # geg. ändern
        # last_end_time
        return self.task_list[-1].end

    # def get_critical_path(self) -> list[ScheduledTask]:
    #     self.get_saz_sez()
    #     return [task for task in self.task_list if task.start == task.saz]

    # def get_saz_sez(self):
    #     self.task_list[-1].saz = self.task_list[-1].start
    #     self.task_list[-1].sez = self.task_list[-1].end

    #     # Frühester Anfangs und Endzeitpunkt
    #     for task in reversed(self[:-1]):
    #         # finde Nachfolgertasks nachfolger im job und nachfolger auf maschine
    #         successor_job = None
    #         successor_machine = None

    #         for task2 in reversed(self):
    #             if (
    #                 task2.machine_id == task.machine_id
    #                 and task2.task_on_machine_idx == (task.task_on_machine_idx + 1)
    #             ):
    #                 successor_machine = task2
    #             if task2.job_id == task.job_id and task2.task_id == (task.task_id + 1):
    #                 successor_job = task2

    #         if successor_job is None and successor_machine is None:
    #             task.sez = self[-1].sez

    #         elif successor_job is None:
    #             task.sez = successor_machine.saz

    #         elif successor_machine is None:
    #             task.sez = successor_job.saz

    #         else:
    #             task.sez = min(successor_machine.saz, successor_job.saz)

    #         task.saz = task.sez - task.duration

