import itertools
import pickle
from giffler_thompson import giffler_thompson
from jobList import JobList
from Schedule import Schedule


def main(solver, data):
    data = read_data()

    for job_list in data:
        # giffler thompson
        if solver == 'google':
            schedule = 
        elif solver == 'meta':
            schedule = 
        elif solver == 'selektor':
            schedule = 

def read_data():
    # for num_jobs in range(10, 101, 5):
    #    for num_machines in range(5, 26, 5):
    for num_jobs, num_machines in itertools.product(range(10, 101, 5), range(5, 26, 5)):
        data = []
        with open(f"Data/job_data_{num_machines}_{num_jobs}.pkl", "rb") as in_file:
            data: list[JobList] = pickle.load(in_file)   

    return data

if __name__ == "__main__":
    # Setzen eines Solvers # google, meta, selektor
    solver = 'google' 

    main(solver)
