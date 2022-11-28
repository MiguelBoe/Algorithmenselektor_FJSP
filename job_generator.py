import pathlib
import pickle
import random
from jobList import JobList

# Konfigurationsbereich
#----------------------------------------------------------------------------------------------------------------------#
max_job_count = 50
max_machine_count = 15
max_duration = 10
instances_count = 10
data_path = '\\Users\\migue\\PycharmProjects\\Algorithmenselektor_JSP\\data'
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
    with open(f'{data_path}\\data.pkl', 'wb') as out_file:
        pickle.dump(data, out_file)

    print('\nJobs created!')

job_generator(max_job_count, max_machine_count, max_duration, instances_count)