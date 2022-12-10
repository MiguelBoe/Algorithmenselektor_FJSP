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
from scheduling_ortools import *
from scheduling_giffler_thompson import giffler_thompson
import plotly.figure_factory as ff
from scheduling_giffler_thompson import get_predecessor
from tabuSearch import TabuSearch
from jobList import JobList
import pickle
import time
import pathlib
import colorcet as cc
import seaborn as sns
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)


# Konfigurationsbereich
#----------------------------------------------------------------------------------------------------------------------#
# Definition des Dateipfades.
data_path = '\\Users\\migue\\PycharmProjects\\Algorithmenselektor_JSP\\data'

# Auswahl der Instanz des generierten Datensatzes.
source = 'train' # random, train, taillard
instance = None

# Auswahl des Solvers und Definition des Zeitlimits der Planung.
solver = 'meta'  # google, meta
time_limit_in_seconds = 5

# Konfiguration der Metaheuristik.
max_iter = 5 # Maximierung der Iterationen der TabuSearch
priority_rule = 'LRPT' # LPT, SPT, LRPT, SRPT

# Fertigen Ablaufplan im Gantt-Chart visualisieren? Sollte nur bei einzelnen Instanzen gemacht werden.
visualization_mode = False
#----------------------------------------------------------------------------------------------------------------------#

# Erstellung des Ordners, in welchem die Ergebnisse abgespeichert sind.
pathlib.Path(f'{data_path}\\results').mkdir(parents=True, exist_ok=True)

# Einlesen der Daten.
with open(f'{data_path}\\{source}_data.pkl', 'rb') as in_file:
    data = pickle.load(in_file)

results = pd.DataFrame()
for instance in range(len(data)):
    # Auswahl des Solvers mit entsprechendem Konfigurationsparameter.
    if solver == "google":
        # Ausführung Google CP_Solver.
        assigned_jobs, all_machines, google_makespan = ortools_scheduler(data=data[instance].list_of_jobs, time_limit_in_seconds=time_limit_in_seconds)
        # Transformation der Daten in das richtige Format für die Visualisierung der Planung mit Hilfe von Plotly in einem Gantt-Diagramm.
        schedule_list = visualize_schedule(assigned_jobs=assigned_jobs, all_machines=all_machines, plan_date=0)
    elif solver == "meta":
        # Starten des Timers.
        timeout = time.time() + time_limit_in_seconds
        # Generierung einer Startlösung mit dem Verfahren von Giffler & Thompson.
        init_schedule = giffler_thompson(data[instance], priority_rule)
        # Durchführung der TabuSearch mit Hilfe der gefundenen initial Lösung. Ausgabe = Beste gefundene Lösung.
        best_solution = TabuSearch(current_solution=init_schedule, max_iter=max_iter, tabu_list_length=int((len(data[instance].list_of_jobs)+data[instance].num_machines)/2), time_limit_in_seconds=time_limit_in_seconds).smart_solve(timeout)
        # Transformation der Daten in das richtige Format für die Visualisierung der Planung mit Hilfe von Plotly in einem Gantt-Diagramm.
        schedule_list = get_schedule_list(best_solution.schedule)
        print(f'Best solution with TabuSearch found with a makespan of {best_solution.makespan}')

    # Visualisierng der Planung mit Hilfe von Plotly in einem Gantt-Diagramm.
    if visualization_mode:
        fig = ff.create_gantt(schedule_list, index_col="Resource", show_colorbar=True, group_tasks=True, colors=sns.color_palette(cc.glasbey, n_colors=(len(data[instance].list_of_jobs))))
        fig.layout.xaxis.type = "linear"
        fig.show()

    if solver == 'meta':
        results = results.append({'Instanz':instance, 'Makespan': best_solution.makespan}, ignore_index=True)
    elif solver == 'google':
        results = results.append({'Instanz': instance, 'Makespan': google_makespan}, ignore_index=True)
    print(f'Instance {instance} done!')

results.to_csv(f'{data_path}\\results\\{source}_results_{solver}.csv', sep=',')


