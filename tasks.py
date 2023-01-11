class Task:
    _id: int = 0

    def __init__(
        self, machine_id: int, job_id: int, duration: int, task_id: int
    ) -> None:
        self.machine_id = machine_id
        self.job_id = job_id
        self.duration = duration
        self.task_id = task_id
        self.id = Task._id
        Task._id += 1


class ScheduledTask(Task):
    def __init__(
        self,
        machine_id: int,
        job_id: int,
        duration: int,
        task_id: int,
        start: int,
        end: int,
        task_on_machine_idx: int,
        saz: int = 0,
        sez: int = 0,
    ) -> None:
        super().__init__(machine_id, job_id, duration, task_id)

        self.start = start
        self.end = end
        self.task_on_machine_idx = task_on_machine_idx
        self.saz = saz
        self.sez = sez
