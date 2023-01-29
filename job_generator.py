"""
@author: böttcher & pretz

#-----------------------------------------------------------------------------#
#         Projektseminar Business Analytics - Wintersemester 22/23            #
#-----------------------------------------------------------------------------#
#                                                                             #
#                               Jobgenerator                                  #
#                Generierung/Einlesen von Job-Shop-Instanzen                  #
#                                                                             #
#                                                                             #
#-----------------------------------------------------------------------------#
"""

import pathlib
import pickle
import random
import glob
from jobList import JobList


def job_generator_random(
    max_job_count: int, max_machine_count: int, max_duration: int, instances_count: int, data_path: str
):

    """Generieren von Instanzen unterschiedlicher, zufälliger Joblänge innnerhalb einer Instanz"""

    data = []
    for _ in range(instances_count):
        num_jobs = random.randint(2, max_job_count)
        num_machines = random.randint(2, max_machine_count)
        jobs_data = JobList.create(max_duration, num_machines, num_jobs, "random")
        data.append(jobs_data)

    # Erstellen des Ordners, falls dieser nicht existiert
    pathlib.Path(data_path).mkdir(parents=True, exist_ok=True)
    # Safe data
    with open(f"{data_path}\\random_data.pkl", "wb") as out_file:
        pickle.dump(data, out_file)

    print("\nJobs created!")


def job_generator_train_or_test(
    num_jobs: list[int],
    num_machines: list[int],
    max_duration_train: int,
    instances_count_per_combination: int,
    source: str,
    data_path: str,
):

    """Generieren von Instanzen in denen Joblänge = Maschinenanzahl ist"""

    data = []
    for machines in num_machines:
        for jobs in num_jobs:
            for _ in range(instances_count_per_combination):
                jobs_data = JobList.create(max_duration_train, machines, jobs, source)
                data.append(jobs_data)

    # Erstellen des Ordners, falls dieser nicht existiert
    pathlib.Path(data_path).mkdir(parents=True, exist_ok=True)
    # Safe data
    with open(f"{data_path}\{source}_data.pkl", "wb") as out_file:
        pickle.dump(data, out_file)

    print("\nJobs created!")


def get_extern_instances(data_path: str, source: str):

    """Einlesen externer Instanzen und in das erforderliche Format transformieren. Dies wurde hauptsächlich für die Taillard-Instanzen benutzt."""
    # x i muss noch ersetzt werden
    data = []
    taillard_files = glob.glob(f"{data_path}\{source}_instances\*")
    for file in taillard_files:
        with open(file) as file:
            instance = []
            for line in file:
                job = [int(x) for x in line.split()]
                job_tuple_format = [(job[i], job[i + 1]) for i in range(0, len(job), 2)]
                instance.append(job_tuple_format)
            instance = JobList(instance)
        data.append(instance)

    # Erstellen des Ordners, falls dieser nicht existiert
    pathlib.Path(data_path).mkdir(parents=True, exist_ok=True)
    # Safe data
    with open(f"{data_path}\\{source}_data.pkl", "wb") as out_file:
        pickle.dump(data, out_file)

    print("\nJobs transformed!")


if __name__ == "__main__":

    # Auswahl des Instanzgenerators.
    source = "test"  # random, train, test, taillard

    if source == "random":

        job_generator_random(
            max_job_count=50, max_machine_count=15, max_duration=10, instances_count=10, data_path=".\\data"
        )

    elif source in {"train", "test"}:

        job_generator_train_or_test(
            num_jobs=[15, 20, 30, 50, 100],
            num_machines=[15, 20],
            max_duration_train=100,
            instances_count_per_combination=3,
            source=source,
            data_path=".\\data",
        )

    else:

        data = get_extern_instances(data_path=".\\data", source="taillard")
