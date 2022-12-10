import pathlib
import pickle
import random
import glob
from jobList import JobList


#Auswahl der Instanzen und Definition des Dateipfades.
#----------------------------------------------------------------------------------------------------------------------#
source = 'taillard' # train, taillard
data_path = '\\Users\\migue\\PycharmProjects\\Algorithmenselektor_JSP\\data'
#----------------------------------------------------------------------------------------------------------------------#


# Konfigurationsbereich für den job_generator
#----------------------------------------------------------------------------------------------------------------------#
max_job_count = 50
max_machine_count = 15
max_duration = 10
instances_count = 10
#----------------------------------------------------------------------------------------------------------------------#


# Create directory if it doesn't exist
pathlib.Path(data_path).mkdir(parents=True, exist_ok=True)

# Mit Hilfe des Job Generators werden verschiedene Instanzen auf Basis der angegebenen Parameter generiert.
def job_generator(max_job_count, max_machine_count, max_duration, instances_count):

    data = []
    for i in range(instances_count):
        # Anzahl der Jobs
        num_jobs = random.randint(2, max_job_count)
        # Anzahl der Maschinen
        num_machines = random.randint(2, max_machine_count)
        # Generierung eines Objekts
        jobs_data = JobList.create(max_duration, num_machines, num_jobs)
        data.append(jobs_data)

    # Safe data
    with open(f'{data_path}\\train_data.pkl', 'wb') as out_file:
        pickle.dump(data, out_file)

    print('\nJobs created!')

def get_taillard_instances(data_path):
    data = []
    taillard_files = glob.glob(f'{data_path}\\taillard_instances\\*')
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
    with open(f'{data_path}\\taillard_data.pkl', 'wb') as out_file:
        pickle.dump(data, out_file)

    print('\nJobs created!')


if source == 'train':
    job_generator(max_job_count, max_machine_count, max_duration, instances_count)
elif source == 'taillard':
    data = get_taillard_instances(data_path)