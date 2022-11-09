"""
@author: pretz & böttcher

#-----------------------------------------------------------------------------#
#         Projektseminar Business Analytics - Wintersemester 22/23            #
#-----------------------------------------------------------------------------#
#                      CP Solver - Ortools by google                          #
#                                                                             #      
#-----------------------------------------------------------------------------#
"""
import random
from typing import Tuple


def generate_jobs(
    num_jobs: int, max_tasks: int, duration_range: Tuple, num_machines: int
):
    all_jobs = []
    for _ in range(num_jobs):
        # liste die mindestens aus einem bis num_machines Elementen besteht und die Machinennummern zwischen 0 und num_machines enthält
        machines_list = list(range(random.randint(1, num_machines)))

        # aus dieser Liste werden zufällig Elemente gewählt (Wenn die Liste nur 1 Element hat, wird dieses gewählt)
        machine_num_list = random.sample(
            machines_list, min(len(machines_list), random.randint(1, max_tasks))
        )

        # mit zufälliger Bearbeitungsdauer versehen und an die Liste anhängen
        all_jobs.append(
            [
                (machine_num, random.randint(duration_range[0], duration_range[1]))
                for machine_num in machine_num_list
            ]
        )
    return all_jobs


def main():
    num_jobs = 5

    # num tasks = num maschinen oder tasks < maschinen
    max_tasks = 5
    num_machines = 5

    duration_range = (1, 10)

    all_jobs = generate_jobs(
        num_jobs=num_jobs,
        max_tasks=max_tasks,
        duration_range=duration_range,
        num_machines=num_machines,
    )
    print(all_jobs)


if __name__ == "__main__":
    main()

