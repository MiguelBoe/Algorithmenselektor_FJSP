import random
from typing import Tuple


class JobList:
    def __init__(self, list_of_jobs: list[list[Tuple[int, int]]]):

        self.list_of_jobs = list_of_jobs

        self.num_machines = self.get_num_machines()
        self.job_durations = self.get_processing_time()
        self.job_length = self.get_job_length()

    def __str__(self) -> str:
        return str(self.list_of_jobs)

    def __repr__(self) -> str:
        return self.__str__()

    def __len__(self) -> int:
        return len(self.list_of_jobs)

    def get_num_machines(self) -> int:
        """
        Rausschreiben der Anzahl der Maschinen dieser Instanz.
        """
        num_machines = 0
        for job in self.list_of_jobs:
            for task in job:
                if task[0] > num_machines:
                    num_machines = task[0]

        return num_machines + 1

    def get_processing_time(self) -> list:
        """ Berechnen der Jobdauer für jeden Job der Instanz. """
        return [sum(task[1] for task in job) for job in self.list_of_jobs]

    def get_job_length(self) -> list:
        """ Berechnen der Anzahl der Tasks in einem Job für jeden Job. """
        return [len(job) for job in self.list_of_jobs]

    @classmethod
    def create(cls, max_duration, num_machines, num_jobs):
        """
        Erstellen eines Jobs, bestehend aus mehreren Tasks.

        Parameters
        ----------
        max_duration : Int
            Maximale Dauer eines Tasks in dem Job.

        num_machines : Int
            Anzahl der verfügbaren Maschinen.

        max_tasks : Int
            Maximale Anzahl an Tasks in einem generierten Job.

        Returns
        -------
        job : list
            Liste bestehend aus Tupeln.
            Die Liste stellt einen Job dar, der aus mehreren Taks (Tupel) besteht.
            Jedes Tupel ist in der Form ( Maschine, Dauer ) gespeichert und stellt einen Task dar.

        """
        list_of_jobs = []

        for _ in range(num_jobs):

            # Zufällige Anzahl der Tasks in dem Job (min 1 Task, max so viele wie Maschinen)
            num_tasks = random.randint(2, num_machines)

            # Liste der verfügbaren Maschinen
            machine_list = list(range(num_machines))

            # Shuffeln der Liste um unterschiedliche Reihenfolgen der Tasks auf den Maschinen zu gewehrleisten
            random.shuffle(machine_list)

            job = []

            # Erstellen der Tasks mit zugehöriger Maschine und Dauer
            for task_idx in range(num_tasks):

                # Dauer des Tasks
                duration = random.randint(1, max_duration)

                # Maschine auf der der Tasks abgearbeitet werden soll
                machine_id = machine_list[task_idx]

                # Erstellen des Tasks
                task = (machine_id, duration)

                # Zusammenstellen des Jobs
                job.append(task)

            # Zusammenstellen der Instanz
            list_of_jobs.append(job)

        return cls(list_of_jobs)