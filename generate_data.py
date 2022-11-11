import pickle
import random
from jobList import JobList


def main():
    data = []
    # num tasks = num maschinen oder tasks < maschinen
    # max_tasks = 5
    max_duration = 10

    for _ in range(50):
        # Anzahl der Jobs
        num_jobs = random.randint(2, 5)

        # Anzahl der Maschinen
        num_machines = random.randint(1, 5)

        jobs_data = JobList.create(max_duration, num_machines, num_jobs)

        data.append(jobs_data)

    with open("job_data.pkl", "wb") as out_file:
        pickle.dump(data, out_file)

    # lesen der Datei
    with open("job_data.pkl", "rb") as in_file:
        data = pickle.load(in_file)

    print(data)


if __name__ == "__main__":
    main()
