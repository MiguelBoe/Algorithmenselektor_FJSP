import pickle
import pandas as pd
import numpy as np
from imblearn.over_sampling import RandomOverSampler
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

data_path = '\\Users\\migue\\PycharmProjects\\Algorithmenselektor_JSP\\data'

def get_instance_features(data_path, source):

    with open(f'{data_path}\\{source}_data.pkl', 'rb') as in_file:
        data = pickle.load(in_file)

    results_meta = pd.read_csv(f'{data_path}\\results\\{source}_results_meta.csv', sep=',', index_col=0)
    results_google = pd.read_csv(f'{data_path}\\results\\{source}_results_google.csv', sep=',', index_col=0)
    results_meta = results_meta.rename(columns={'Makespan': 'meta'})
    results_google = results_google.rename(columns={'Makespan': 'google'})

    results = pd.merge(results_meta, results_google, on='Instanz')
    results['meta_better'] = np.NaN

    for index, row in results.iterrows():
        if row['meta'] < row['google']:
            results['meta_better'].iat[index] = 1
        else:
            results['meta_better'].iat[index] = 0

    instance_features = pd.DataFrame()
    for i in range(len(data)):
        instance = data[i]
        instance_features = instance_features.append({'num_machines': instance.num_machines,
                                                      'num_jobs': len(instance.list_of_jobs),
                                                      'avg_job_duration': np.mean(instance.job_durations),
                                                      'min_job_duration': min(instance.job_durations),
                                                      'max_job_duration': max(instance.job_durations),
                                                      'num_jobs/num_machines': len(instance.list_of_jobs) / instance.num_machines,
                                                      'meta_better': results['meta_better'].iat[i]}, ignore_index=True)

    instance_features['meta_better'] = instance_features['meta_better'].astype(int)

    return instance_features

#train_instance_features = get_instance_features(data_path=data_path, source='train')
test_instance_features = get_instance_features(data_path=data_path, source='taillard')


X_train = train_instance_features[['num_machines', 'num_jobs', 'avg_job_duration', 'min_job_duration', 'max_job_duration', 'num_jobs/num_machines']]
y_train = train_instance_features['meta_better']

X_test = test_instance_features[['num_machines', 'num_jobs', 'avg_job_duration', 'min_job_duration', 'max_job_duration', 'num_jobs/num_machines']]
y_test = test_instance_features['meta_better']


def oversampling(X_train, y_train):
    rus = RandomOverSampler(random_state=0)
    X_train, y_train = rus.fit_resample(X_train, y_train)
    return X_train, y_train

X_train, y_train = undersampling(X_train, y_train)

def random_forest(X_train, X_test, y_train, y_test ):

    random_forest_model = RandomForestClassifier(max_depth=10).fit(X_train, y_train)

    results = pd.DataFrame(random_forest_model.predict(X_test), index=X_test.index)
    results['y_test'] = y_test

    score = accuracy_score(results['y_test'], results[0])

    return results, score

results, score = random_forest(X_train, X_test, y_train, y_test )
print()
