import pickle
import pathlib
import pandas as pd
import numpy as np
import math
from sklearn.model_selection import train_test_split
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
validate_test_set = False
#----------------------------------------------------------------------------------------------------------------------#

pathlib.Path(models_path).mkdir(parents=True, exist_ok=True)

# Initialisierung der Klasse AlgorithmSelector. Diese Klasse hat zwei Modi: 'train' und 'selector.
class AlgorithmSelector:
    def __init__(self, mode, data_path, results_path, instance, model, train_source, test_source, validate_test_set):
        self.mode = mode
        self.data_path = data_path
        self.results_path = results_path
        # Modus 'train' wird angewendet, wenn die Datei algorithmSelector.py ausgeführt wird. In diesem Fall wird das Modell anhand des Trainings-Sets trainiert.
        if mode == 'train':
            self.train_source = train_source
            self.test_source = test_source
            self.validate_test_set = validate_test_set
        # Modus 'selector' wird angewendet, wenn die Klasse ausgehend von der main.py Datei initilisiert wird. In diesem Fall soll mit dem bestehenden Modell und einer gegebenen Instanz eine Vorhersage getätigt werden.
        elif mode == 'selector':
            self.instance = instance
            self.model = model
            self.source = test_source

    # Diese Funktion führt das Training des Modells aus.
    def training(self):
        # Das Trainings- und Test-Set werden eingelesen. Das Test-Set wird nur eingelesen, damit spezifischere Tests und Validierungen durchgeführt werden können.
        # Mit dem train_test_split kann jedoch auch ein Test-Set aus dem Trainings-Set generiert werden.
        with open(f'{self.data_path}\\{self.train_source}_data.pkl', 'rb') as in_file:
            self.train_data = pickle.load(in_file)
        with open(f'{self.data_path}\\{self.test_source}_data.pkl', 'rb') as in_file:
            self.test_data = pickle.load(in_file)
        # Die Funktion get_instance_features() wird dafür verwendet, um Attribute von den Instanzen abzuleiten und ein Trainings- bzw. Test-Set zu generieren, mit welchem ein ML-Modell trainiert, bzw. validiert werden kann.
        self.train_set = self.get_instance_features(self, data = self.train_data, results=self.get_results(self, data = self.train_data, source = self.train_source))
        self.test_set = self.get_instance_features(self, data = self.test_data, results=self.get_results(self, data = self.test_data, source = self.test_source))
        # Die Modellattribute werden definiert.
        self.define_attributes()
        # Für das Training des Modells wird für das Trainings-Set ein Oversampling vorgenommen. Dies ist jedoch nicht zwingend erfoderlich, da die Datenpunkte bzgl. der Zielvariablen relativ ausgeglichen verteilt sind.
        self.oversampling()
        # Das Random Forest-Modell wird trainiert.
        self.random_forest()
        # Das trainierte Modell wird abgespeichert.
        with open(f'{models_path}\\random_forest.pkl', 'wb') as out_file:
            pickle.dump(self.random_forest_model, out_file)
        print('\nTraining done!')

    # Mit dieser Funktion wird eine Prognose mit dem trainierten Modell für die übergebene Instanz generiert.
    def get_selection(self):
        # Zuerst wird wieder ein Datensatz generiert, welcher von dem Modell verarbeitet werden kann.
        self.X = self.get_instance_features(self, data = self.instance, results = None)
        # Anschließend wird mit dem Modell die Prognose durchgeführt, welches Lösungsverfahren besser geeignet ist.
        self.result = int(self.model.predict(self.X)[0])
        return self.result

    # Diese Funktion wird dafür verwendet, um Attribute von den Instanzen abzuleiten und ein Trainings- bzw. Test-Set zu generieren, mit welchem ein ML-Modell trainiert, bzw. validiert werden kann.
    def get_instance_features(self, request, data, results):
        if self.mode == 'selector':
            data = [data]
        instance_features = pd.DataFrame()
        for i in range(len(data)):
            instance = data[i]
            duration_intervals = self.get_duration_intervals(instance=instance)
            percent_conflicts = self.get_conflicts(instance=instance)
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
                        'task_with_duration_[>100]': duration_intervals[11],
                        'percent_conflicts': percent_conflicts}
            if self.mode == 'train': features.update({'meta_better': results['meta_better'].iat[i]})
            instance_features = instance_features.append(features, ignore_index=True)
        if self.mode == 'train': instance_features['meta_better'] = instance_features['meta_better'].astype(int)
        return instance_features

    # Diese Funktion wird dafür verwendet, um die Resultet der Lösungsverfahren zu verarbeiten, damit die Zielvariable definiert werden kann, welche angibt, welches Verfahren die jeweilige Instanz besser lösen konnte.
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

    # Diese Funktion wird dafür verwendet um die Attribute für die Anzahl der Vorgänge pro Zeitintervall zu definieren.
    def get_duration_intervals(self, instance):
        duration_intervals = {1:0,2:0,3:0,4:0,5:0,6:0,7:0,8:0,9:0,10:0,11:0}
        for job in instance.list_of_jobs:
            for task in job:
                duration = task[1]
                duration_intervals[min(math.ceil(duration/10),11)] += 1
        duration_intervals = {k: round((duration_intervals[k]/(instance.num_machines*len(instance.list_of_jobs)))*100,3) for k in duration_intervals.keys()}
        return duration_intervals

    # Diese Funktion bestimmt die prozentuale Anzahl der Konflikte der Vorgänge. Genauer gesagt wird bestimmt, wie viele Jobs, bezogen auf die Maschinenreihenfolge, sich überschneiden.
    def get_conflicts(self, instance):
        conflicts = {}
        for i in range(instance.num_machines):
            conflicts.update({i:(len(instance)-len(set([j[i][0] for j in instance.list_of_jobs])))})
        num_conflicts = sum(conflicts.values())
        percent_conflicts = round((num_conflicts/(len(instance)*instance.num_machines))*100,2)
        return percent_conflicts

    # Mit dieser Funktion werden die Modellattribute für das Trainings definiert.
    # Außerdem wird überprüft, ob ein train_test_split anhand des Trainings-Sets durchgeführt werden soll oder ob ein sepzifisches Test-Set für die Validierung verwendet werden soll.
    def define_attributes(self):
        self.attributes = ['num_machines', 'num_jobs', 'avg_job_duration', 'min_job_duration', 'max_job_duration',
                           'task_with_duration_[0:10]', 'task_with_duration_[11:20]', 'task_with_duration_[21:30]', 'task_with_duration_[31:40]',
                           'task_with_duration_[41:50]', 'task_with_duration_[51:60]', 'task_with_duration_[61:70]', 'task_with_duration_[71:80]',
                           'task_with_duration_[81:90]', 'task_with_duration_[91:100]', 'task_with_duration_[>100]']

        self.X_train = self.train_set[self.attributes]
        self.y_train = self.train_set['meta_better']

        if validate_test_set:
            self.X_test = self.test_set[self.attributes]
            self.y_test = self.test_set['meta_better']
        else:
            self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(self.X_train, self.y_train, test_size=0.1, random_state=0)

    # Mit dieser Funktion wird für das Trainings-Set ein Oversampling vorgenommen. Dies ist jedoch nicht zwingend erfoderlich, da die Datenpunkte bzgl. der Zielvariablen relativ ausgeglichen verteilt sind.
    def oversampling(self):
        rus = RandomOverSampler(random_state=0)
        self.X_train, self.y_train = rus.fit_resample(self.X_train, self.y_train)

    # Mit dieser Funktion wird das Random Forest-Modell trainiert.
    def random_forest(self):
        self.random_forest_model = make_pipeline(StandardScaler(), RandomForestClassifier(max_depth=10, random_state=0)).fit(self.X_train, self.y_train)
        self.results = pd.DataFrame({'prediction':self.random_forest_model.predict(self.X_test)}, index=self.X_test.index)
        self.results['y_test'] = self.y_test
        self.score = accuracy_score(self.results['y_test'], self.results['prediction'])


# Modus 'train' wird angewendet, wenn die Datei algorithmSelector.py ausgeführt wird. In diesem Fall wird das Modell anhand des Trainings-Sets trainiert.
if __name__ == "__main__":
    AlgorithmSelector(mode = 'train', data_path = data_path, results_path = results_path, instance = None, model = None, train_source = train_source, test_source = test_source, validate_test_set=validate_test_set).training()
