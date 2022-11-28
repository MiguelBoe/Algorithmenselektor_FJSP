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

from utils import *
from scheduling_ortools import *
from scheduling_giffler_thompson import giffler_thompson
import plotly.figure_factory as ff
from scheduling_giffler_thompson import get_predecessor
from tabuSearch import TabuSearch
from jobList import JobList
import pickle
import time
import colorcet as cc
import seaborn as sns


# Konfigurationsbereich
#----------------------------------------------------------------------------------------------------------------------#
# Auswahl des Solvers und Definition des Zeitlimits der Planung.
solver = 'meta'  # google, meta
time_limit_in_seconds = 10

# Maximierung der Iterationen der TabuSearch.
max_iter = 10000

# Auswahl der Instanz des generierten Datensatzes.
instance = 0

# Definition des Pfades, an welchem die Daten abgespeichert sind.
data_path = '\\Users\\migue\\PycharmProjects\\Algorithmenselektor_JSP\\data'
#----------------------------------------------------------------------------------------------------------------------#


# Einlesen der Daten.
with open(f'{data_path}\\data.pkl', 'rb') as in_file:
    data = pickle.load(in_file)

# Kleine Test-Instanz.
# data = [  # task = (machine_id, processing_time).
#     [(0, 5), (1, 3), (2, 3), (3, 2)],  # Job0
#     [(1, 4), (0, 7), (2, 8), (3, 6)],  # Job1
#     [(3, 3), (2, 5), (1, 6), (0, 1)],  # Job2
#     [(2, 4), (3, 7), (1, 1), (0, 2)],  # Job2
# ]
# data = JobList(data)

# Auswahl des Solvers mit entsprechendem Konfigurationsparameter.
if solver == "google":
    # Ausführung Google CP_Solver.
    assigned_jobs, all_machines = ortools_scheduler(data=data[instance].list_of_jobs, time_limit_in_seconds=time_limit_in_seconds)
    # Transformation der Daten in das richtige Format für die Visualisierung der Planung mit Hilfe von Plotly in einem Gantt-Diagramm.
    schedule_list = visualize_schedule(assigned_jobs=assigned_jobs, all_machines=all_machines, plan_date=0)
elif solver == "meta":
    # Generierung einer Startlösung mit dem Verfahren von Giffler & Thompson.
    init_schedule = giffler_thompson(data[instance])
    # Durchführung der TabuSearch mit Hilfe der gefundenen initial Lösung. Ausgabe = Beste gefundene Lösung.
    best_solution = TabuSearch(current_solution=init_schedule, max_iter=max_iter, tabu_list_length=int((len(data[instance].list_of_jobs)+data[instance].num_machines)/2), time_limit_in_seconds=time_limit_in_seconds).solve()
    # Transformation der Daten in das richtige Format für die Visualisierung der Planung mit Hilfe von Plotly in einem Gantt-Diagramm.
    schedule_list = get_schedule_list(best_solution.schedule)
    print(f'\nBest solution with TabuSearch found with a makespan of {best_solution.makespan}')

# Visualisierng der Planung mit Hilfe von Plotly in einem Gantt-Diagramm.
fig = ff.create_gantt(schedule_list, index_col="Resource", show_colorbar=True, group_tasks=True, colors=sns.color_palette(cc.glasbey, n_colors=(len(data[instance].list_of_jobs))))
fig.layout.xaxis.type = "linear"
fig.show()