"""
@author: pretz & böttcher

#-----------------------------------------------------------------------------#
#         Projektseminar Business Analytics - Wintersemester 22/23            #
#-----------------------------------------------------------------------------#
#                                                                             #
#                                 Main File                                   #
#                                                                             #
#-----------------------------------------------------------------------------#
"""

import pandas as pd
from utils import *
from cp_solver import *
from giffler_thompson import giffler_thompson
import plotly.figure_factory as ff
from giffler_thompson import get_predecessor
from tabuSearch import TabuSearch
from jobList import JobList
from algorithmSelector import AlgorithmSelector
import pickle
import time
import pathlib
import colorcet as cc
import seaborn as sns
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)


# Konfigurationsbereich
#----------------------------------------------------------------------------------------------------------------------#
# Definition der Dateipfade.
data_path = '\\Users\\migue\\PycharmProjects\\Algorithmenselektor_JSP\\data'
results_path = '\\Users\\migue\\PycharmProjects\\Algorithmenselektor_JSP\\results'
models_path = '\\Users\\migue\\PycharmProjects\\Algorithmenselektor_JSP\\models'

# Auswahl der Instanz des generierten Datensatzes.
source = 'taillard' # random, train, taillard
instance = None

# Auswahl des Solvers und Definition des Zeitlimits der Planung.
solver = 'algorithm_selector'  # google, meta, algorithm_selector
time_limit_in_seconds = 5

# Konfiguration der Metaheuristik.
max_iter = 5 # Maximierung der Iterationen der TabuSearch
priority_rule = 'LRPT' # LPT, SPT, LRPT, SRPT

# Fertigen Ablaufplan im Gantt-Chart visualisieren? Sollte nur bei einzelnen Instanzen gemacht werden.
visualization_mode = False
#----------------------------------------------------------------------------------------------------------------------#

# Erstellung des Ordners, in welchem die Ergebnisse abgespeichert sind.
pathlib.Path(f'{results_path}\\reports').mkdir(parents=True, exist_ok=True)
pathlib.Path(f'{results_path}\\schedules').mkdir(parents=True, exist_ok=True)
pathlib.Path(models_path).mkdir(parents=True, exist_ok=True)

# Einlesen der Daten.
with open(f'{data_path}\\{source}_data.pkl', 'rb') as in_file:
    data = pickle.load(in_file)

if solver == 'algorithm_selector':
    with open(f'{models_path}\\random_forest.pkl', 'rb') as in_file:
        model = pickle.load(in_file)

results = pd.DataFrame()
schedule = {}
for instance in range(len(data)):
    # Auswahl des Solvers mit entsprechendem Konfigurationsparameter.
    if solver == "google":
        # Ausführung Google CP_Solver.
        assigned_jobs, all_machines, makespan = ortools_scheduler(data=data[instance].list_of_jobs, time_limit_in_seconds=time_limit_in_seconds)
        # Transformation der Daten in das richtige Format für die Visualisierung der Planung mit Hilfe von Plotly in einem Gantt-Diagramm.
        schedule_list = visualize_schedule(assigned_jobs=assigned_jobs, all_machines=all_machines, plan_date=0)
    elif solver == "meta":
        # Starten des Timers.
        timeout = time.time() + time_limit_in_seconds
        # Generierung einer Startlösung mit dem Verfahren von Giffler & Thompson.
        init_solution = giffler_thompson(data[instance], priority_rule)
        # Durchführung der TabuSearch mit Hilfe der gefundenen initial Lösung. Ausgabe = Beste gefundene Lösung.
        best_solution = TabuSearch(current_solution=init_solution, max_iter=max_iter, tabu_list_length=int((len(data[instance].list_of_jobs)+data[instance].num_machines)/2), time_limit_in_seconds=time_limit_in_seconds).smart_solve(timeout)
        # Transformation der Daten in das richtige Format für die Visualisierung der Planung mit Hilfe von Plotly in einem Gantt-Diagramm.
        schedule_list = get_schedule_list(best_solution.schedule)
        makespan = best_solution.makespan
        print(f'Best solution with TabuSearch found with a makespan of {makespan}')
    elif solver == 'algorithm_selector':
        timeout = time.time() + time_limit_in_seconds
        selection = AlgorithmSelector(mode = 'test', data_path = data_path, results_path = results_path, instance=data[instance], model = model, train_source = None, test_source = source).get_selection()
        if selection == 0:
            assigned_jobs, all_machines, makespan = ortools_scheduler(data=data[instance].list_of_jobs, time_limit_in_seconds=time_limit_in_seconds)
            schedule_list = visualize_schedule(assigned_jobs=assigned_jobs, all_machines=all_machines, plan_date=0)
        elif selection == 1:
            init_solution = giffler_thompson(data[instance], priority_rule)
            best_solution = TabuSearch(current_solution=init_solution, max_iter=max_iter, tabu_list_length=int((len(data[instance].list_of_jobs) + data[instance].num_machines) / 2), time_limit_in_seconds=time_limit_in_seconds).smart_solve(timeout)
            schedule_list = get_schedule_list(best_solution.schedule)
            makespan = best_solution.makespan
            print(f'Best solution with TabuSearch found with a makespan of {makespan}')

    # Visualisierng der Planung mit Hilfe von Plotly in einem Gantt-Diagramm.
    if visualization_mode:
        fig = ff.create_gantt(schedule_list, index_col="Resource", show_colorbar=True, group_tasks=True, colors=sns.color_palette(cc.glasbey, n_colors=(len(data[instance].list_of_jobs))))
        fig.layout.xaxis.type = "linear"
        fig.show()

    if solver == 'algorithm_selector': results = results.append({'Instanz':instance, 'Makespan': makespan, 'Solver': selection}, ignore_index=True)
    else: results = results.append({'Instanz':instance, 'Makespan': makespan}, ignore_index=True)
    schedule.update({f'Instanz_{instance}': schedule_list})
    print(f'Instance {instance} done!')

results.to_csv(f'{results_path}\\reports\\{source}_report_{solver}.csv', sep=',')
with open(f'{results_path}\\schedules\\{source}_schedule_{solver}.pkl', 'wb') as out_file:
    pickle.dump(schedule, out_file)


