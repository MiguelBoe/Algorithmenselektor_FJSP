import pickle
import pathlib
import pandas as pd
import numpy as np
import math
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from imblearn.over_sampling import RandomOverSampler
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)


# Konfigurationsbereich.
#----------------------------------------------------------------------------------------------------------------------#
data_path = '\\Users\\migue\\PycharmProjects\\Algorithmenselektor_JSP\\data'
results_path = '\\Users\\migue\\PycharmProjects\\Algorithmenselektor_JSP\\results'
models_path = '\\Users\\migue\\PycharmProjects\\Algorithmenselektor_JSP\\models'
train_source = 'train'
test_source = 'test'
#----------------------------------------------------------------------------------------------------------------------#

pathlib.Path(models_path).mkdir(parents=True, exist_ok=True)

class AlgorithmSelector:
    def __init__(self, mode, data_path, results_path, instance, model, train_source, test_source):
        self.mode = mode
        self.data_path = data_path
        self.results_path = results_path
        if mode == 'train':
            self.train_source = train_source
            self.test_source = test_source
        elif mode == 'selector':
            self.instance = instance
            self.model = model
            self.source = test_source


    def training(self):
        with open(f'{self.data_path}\\{self.train_source}_data.pkl', 'rb') as in_file:
            self.train_data = pickle.load(in_file)
        with open(f'{self.data_path}\\{self.test_source}_data.pkl', 'rb') as in_file:
            self.test_data = pickle.load(in_file)
        self.train_set = self.get_instance_features(self, data = self.train_data, results=self.get_results(self, data = self.train_data, source = self.train_source))
        self.test_set = self.get_instance_features(self, data = self.test_data, results=self.get_results(self, data = self.test_data, source = self.test_source))
        self.define_attributes()
        self.oversampling()
        self.random_forest()
        with open(f'{models_path}\\random_forest.pkl', 'wb') as out_file:
            pickle.dump(self.random_forest_model, out_file)
        print('\nTraining done!')


    def get_selection(self):
        self.X = self.get_instance_features(self, data = self.instance, results = None)
        self.result = int(self.model.predict(self.X)[0])
        return self.result


    def get_instance_features(self, request, data, results):
        if self.mode == 'selector':
            data = [data]
        instance_features = pd.DataFrame()
        for i in range(len(data)):
            instance = data[i]
            duration_intervals = self.get_duration_intervals(instance=instance)
            features = {'num_machines': instance.num_machines, 'num_jobs': len(instance.list_of_jobs),
                        'avg_job_duration': np.mean(instance.job_durations),
                        'min_job_duration': min(instance.job_durations),
                        'max_job_duration': max(instance.job_durations),
                        'task_with_duration_[0:10]': duration_intervals[1],
                        'task_with_duration_[11:20]': duration_intervals[2],
                        'task_with_duration_[21:30]': duration_intervals[3],
                        'task_with_duration_[31:40]': duration_intervals[4],
                        'task_with_duration_[41:50]': duration_intervals[5],
                        'task_with_duration_[51:60]': duration_intervals[6],
                        'task_with_duration_[61:70]': duration_intervals[7],
                        'task_with_duration_[71:80]': duration_intervals[8],
                        'task_with_duration_[81:90]': duration_intervals[9],
                        'task_with_duration_[91:100]': duration_intervals[10],
                        'task_with_duration_[>100]': duration_intervals[11]}
            if self.mode == 'train': features.update({'meta_better': results['meta_better'].iat[i]})
            instance_features = instance_features.append(features, ignore_index=True)
        if self.mode == 'train': instance_features['meta_better'] = instance_features['meta_better'].astype(int)
        return instance_features


    def get_results(self, request, data, source):
        results_meta = pd.read_csv(f'{self.results_path}\\reports\\{source}_report_meta.csv', sep=',', index_col=0)
        results_google = pd.read_csv(f'{self.results_path}\\reports\\{source}_report_google.csv', sep=',', index_col=0)
        results_meta = results_meta.rename(columns={'Makespan': 'meta'})
        results_google = results_google.rename(columns={'Makespan': 'google'})
        results = pd.merge(results_meta, results_google, on='Instanz')
        results['meta_better'] = np.NaN
        for index, row in results.iterrows():
            if row['meta'] < row['google']:
                results['meta_better'].iat[index] = 1
            else:
                results['meta_better'].iat[index] = 0
        return results


    def get_duration_intervals(self, instance):
        duration_intervals = {1:0,2:0,3:0,4:0,5:0,6:0,7:0,8:0,9:0,10:0,11:0}
        for job in instance.list_of_jobs:
            for task in job:
                duration = task[1]
                duration_intervals[min(math.ceil(duration/10),11)] += 1
        duration_intervals = {k: round((duration_intervals[k]/(instance.num_machines*len(instance.list_of_jobs)))*100,3) for k in duration_intervals.keys()}
        return duration_intervals


    def define_attributes(self):
        self.X_train = self.train_set[['num_machines', 'num_jobs', 'avg_job_duration', 'min_job_duration', 'max_job_duration',
                               'task_with_duration_[0:10]', 'task_with_duration_[11:20]', 'task_with_duration_[21:30]', 'task_with_duration_[31:40]',
                               'task_with_duration_[41:50]', 'task_with_duration_[51:60]', 'task_with_duration_[61:70]', 'task_with_duration_[71:80]',
                               'task_with_duration_[81:90]', 'task_with_duration_[91:100]', 'task_with_duration_[>100]']]
        self.y_train = self.train_set['meta_better']
        self.X_test = self.test_set[['num_machines', 'num_jobs', 'avg_job_duration', 'min_job_duration', 'max_job_duration',
                               'task_with_duration_[0:10]', 'task_with_duration_[11:20]', 'task_with_duration_[21:30]', 'task_with_duration_[31:40]',
                               'task_with_duration_[41:50]', 'task_with_duration_[51:60]', 'task_with_duration_[61:70]', 'task_with_duration_[71:80]',
                               'task_with_duration_[81:90]', 'task_with_duration_[91:100]', 'task_with_duration_[>100]']]
        self.y_test = self.test_set['meta_better']


    def oversampling(self):
        rus = RandomOverSampler(random_state=0)
        self.X_train, self.y_train = rus.fit_resample(self.X_train, self.y_train)


    def random_forest(self):
        self.random_forest_model = make_pipeline(StandardScaler(), RandomForestClassifier(max_depth=1000, random_state=14)).fit(self.X_train, self.y_train)
        self.results = pd.DataFrame({'prediction':self.random_forest_model.predict(self.X_test)}, index=self.X_test.index)
        self.results['y_test'] = self.y_test
        self.score = accuracy_score(self.results['y_test'], self.results['prediction'])


if __name__ == "__main__":
    AlgorithmSelector(mode = 'train', data_path = data_path, results_path = results_path, instance = None, model = None, train_source = train_source, test_source = test_source).training()
