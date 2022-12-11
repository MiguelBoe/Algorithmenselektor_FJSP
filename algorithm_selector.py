import pickle
import pandas as pd
import numpy as np
import math
from sklearn.model_selection import train_test_split
from imblearn.over_sampling import RandomOverSampler
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)


# Konfigurationsbereich.
#----------------------------------------------------------------------------------------------------------------------#
data_path = '\\Users\\migue\\PycharmProjects\\Algorithmenselektor_JSP\\data'
results_path = '\\Users\\migue\\PycharmProjects\\Algorithmenselektor_JSP\\results'
train = 'train'
test = 'taillard'
#----------------------------------------------------------------------------------------------------------------------#


def get_results(data_path, results_path, source):
    with open(f'{data_path}\\{source}_data.pkl', 'rb') as in_file:
        data = pickle.load(in_file)
    results_meta = pd.read_csv(f'{results_path}\\reports\\{source}_results_meta.csv', sep=',', index_col=0)
    results_google = pd.read_csv(f'{results_path}\\reports\\{source}_results_google.csv', sep=',', index_col=0)
    results_meta = results_meta.rename(columns={'Makespan': 'meta'})
    results_google = results_google.rename(columns={'Makespan': 'google'})
    results = pd.merge(results_meta, results_google, on='Instanz')
    results['meta_better'] = np.NaN
    for index, row in results.iterrows():
        if row['meta'] < row['google']: results['meta_better'].iat[index] = 1
        else: results['meta_better'].iat[index] = 0
    return results


def get_duration_intervals(instance):
    duration_intervals = {1:0,2:0,3:0,4:0,5:0,6:0,7:0,8:0,9:0,10:0,11:0}
    for job in instance.list_of_jobs:
        for task in job:
            duration = task[1]
            duration_intervals[min(math.ceil(duration/10),11)] += 1
    duration_intervals = {k: round((duration_intervals[k]/(instance.num_machines*len(instance.list_of_jobs)))*100,3) for k in duration_intervals.keys()}
    return duration_intervals


def get_instance_features(data_path, source, results):
    with open(f'{data_path}\\{source}_data.pkl', 'rb') as in_file:
        data = pickle.load(in_file)
    instance_features = pd.DataFrame()
    for i in range(len(data)):
        instance = data[i]
        duration_intervals = get_duration_intervals(instance=instance)
        features = {'num_machines': instance.num_machines, 'num_jobs': len(instance.list_of_jobs), 'avg_job_duration': np.mean(instance.job_durations),
                    'min_job_duration': min(instance.job_durations), 'max_job_duration': max(instance.job_durations),
                    'task_with_duration_[0:10]':duration_intervals[1], 'task_with_duration_[11:20]': duration_intervals[2], 'task_with_duration_[21:30]': duration_intervals[3],
                    'task_with_duration_[31:40]': duration_intervals[4], 'task_with_duration_[41:50]': duration_intervals[5], 'task_with_duration_[51:60]': duration_intervals[6],
                    'task_with_duration_[61:70]': duration_intervals[7], 'task_with_duration_[71:80]': duration_intervals[8], 'task_with_duration_[81:90]': duration_intervals[9],
                    'task_with_duration_[91:100]': duration_intervals[10], 'task_with_duration_[>100]': duration_intervals[11], 'meta_better': results['meta_better'].iat[i]}
        instance_features = instance_features.append(features, ignore_index=True)
    instance_features['meta_better'] = instance_features['meta_better'].astype(int)
    return instance_features


def define_attributes(train_set, test_set):
    X_train = train_set[['num_machines', 'num_jobs', 'avg_job_duration', 'min_job_duration', 'max_job_duration',
                           'task_with_duration_[0:10]', 'task_with_duration_[11:20]', 'task_with_duration_[21:30]', 'task_with_duration_[31:40]',
                           'task_with_duration_[41:50]', 'task_with_duration_[51:60]', 'task_with_duration_[61:70]', 'task_with_duration_[71:80]',
                           'task_with_duration_[81:90]', 'task_with_duration_[91:100]', 'task_with_duration_[>100]']]
    y_train = train_set['meta_better']
    X_test = test_set[['num_machines', 'num_jobs', 'avg_job_duration', 'min_job_duration', 'max_job_duration',
                           'task_with_duration_[0:10]', 'task_with_duration_[11:20]', 'task_with_duration_[21:30]', 'task_with_duration_[31:40]',
                           'task_with_duration_[41:50]', 'task_with_duration_[51:60]', 'task_with_duration_[61:70]', 'task_with_duration_[71:80]',
                           'task_with_duration_[81:90]', 'task_with_duration_[91:100]', 'task_with_duration_[>100]']]
    y_test = test_set['meta_better']
    return X_train, X_test, y_train, y_test


def oversampling(X_train, y_train):
    rus = RandomOverSampler(random_state=0)
    X_train, y_train = rus.fit_resample(X_train, y_train)
    return X_train, y_train


def random_forest(X_train, X_test, y_train, y_test ):
    random_forest_model = RandomForestClassifier(max_depth=10).fit(X_train, y_train)
    results = pd.DataFrame({'prediction':random_forest_model.predict(X_test)}, index=X_test.index)
    results['y_test'] = y_test
    score = accuracy_score(results['y_test'], results['prediction'])
    return results, score


train_set = get_instance_features(data_path=data_path, source=train, results = get_results(data_path=data_path, results_path=results_path, source=train))
test_set = get_instance_features(data_path=data_path, source=test, results = get_results(data_path=data_path, results_path=results_path, source=test))
X_train, X_test, y_train, y_test = define_attributes(train_set, test_set)
X_train, y_train = oversampling(X_train, y_train)
results, score = random_forest(X_train, X_test, y_train, y_test )
print('Done!')