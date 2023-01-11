import csv
import pickle
import random
from jobList import JobList
import numpy as np


def main():

    max_duration = 100

    for num_jobs in range(10, 101, 5):
        data = []

        for num_machines in range(5, 26, 5):

            for _ in range(50):
                jobs_data = JobList.create(max_duration, num_machines, num_jobs)

                data.append(jobs_data)

                # speichern der Datei

                with open(
                    f"Data/job_data_{num_machines}_{num_jobs}.pkl", "wb"
                ) as out_file:
                    pickle.dump(data, out_file)

                with open(f"Data/job_data_{num_machines}_{num_jobs}.txt", "w") as fp:
                    for item in data:
                        # write each item on a new line
                        fp.write("%s\n" % item)
            data = []

    print("Done generating Data!")

    # # lesen der Datei
    # with open(f"Data/job_data_{num_machines}_{num_jobs}.pkl", "rb") as in_file:
    #     data = pickle.load(in_file)


if __name__ == "__main__":
    main()
