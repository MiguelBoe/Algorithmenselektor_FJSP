import pathlib
import pickle
import random
import glob
from jobList import JobList


#Auswahl der Instanzen und Definition des Dateipfades.
#----------------------------------------------------------------------------------------------------------------------#
source = 'train' # random, train, taillard
data_path = '\\Users\\migue\\PycharmProjects\\Algorithmenselektor_JSP\\data'
#----------------------------------------------------------------------------------------------------------------------#


# Konfigurationsbereich für den job_generator_random
#----------------------------------------------------------------------------------------------------------------------#
max_job_count = 50
max_machine_count = 15
max_duration_random = 10
instances_count = 10
#----------------------------------------------------------------------------------------------------------------------#


# Konfigurationsbereich für den job_generator_train
#----------------------------------------------------------------------------------------------------------------------#
num_jobs = [15, 20, 30, 50, 100]
num_machines = [15, 20]
max_duration_train = 100
instances_count_per_combination = 300
#----------------------------------------------------------------------------------------------------------------------#


# Create directory if it doesn't exist
pathlib.Path(data_path).mkdir(parents=True, exist_ok=True)

# Mit Hilfe des Job Generators werden verschiedene Instanzen auf Basis der angegebenen Parameter generiert.
def job_generator_random(max_job_count, max_machine_count, max_duration, instances_count):
    data = []
    for i in range(instances_count):
        num_jobs = random.randint(2, max_job_count)
        num_machines = random.randint(2, max_machine_count)
        jobs_data = JobList.create(max_duration, num_machines, num_jobs, source)
        data.append(jobs_data)

    # Safe data
    with open(f'{data_path}\\random_data.pkl', 'wb') as out_file:
        pickle.dump(data, out_file)


def job_generator_train(num_jobs, num_machines, max_duration_train, instances_count_per_combination):
    data = []
    for machines in num_machines:
        for jobs in num_jobs:
            for i in range(instances_count_per_combination):
                jobs_data = JobList.create(max_duration_train, machines, jobs, source)
                data.append(jobs_data)
    # Safe data
    with open(f'{data_path}\\train_data.pkl', 'wb') as out_file:
        pickle.dump(data, out_file)


def get_extern_instances(data_path, source):
    data = []
    taillard_files = glob.glob(f'{data_path}\\{source}_instances\\*')
    for file in taillard_files:
        with open(file) as f:
            instance = []
            num_jobs, num_machines = [int(x) for x in next(f).split()]
            for line in f:
                job = [int(x) for x in line.split()]
                job_tuple_format = [(job[i], job[i + 1]) for i in range(0, len(job), 2)]
                instance.append(job_tuple_format)
            instance = JobList(instance)
        data.append(instance)

    # Safe data
    with open(f'{data_path}\\{source}_data.pkl', 'wb') as out_file:
        pickle.dump(data, out_file)


if source == 'random':
    job_generator_random(max_job_count, max_machine_count, max_duration_random, instances_count)
elif source == 'train':
    job_generator_train(num_jobs, num_machines, max_duration_train, instances_count_per_combination)
else:
    data = get_extern_instances(data_path, source)

print('\nJobs created!')