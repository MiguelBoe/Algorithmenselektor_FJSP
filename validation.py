import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pickle
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

# Konfigurationsbereich.
#----------------------------------------------------------------------------------------------------------------------#
source = 'taillard'
#----------------------------------------------------------------------------------------------------------------------#

# Paths.
directory = os.getcwd()
results_path = f'{directory}\\results'

def algorithm_selector_validation(source, directory, results_path):
    # Read reports.
    results_algorithm_selector = pd.read_csv(f'{results_path}\\reports\\{source}_report_algorithm_selector.csv', sep=',', index_col=0)
    results_google = pd.read_csv(f'{results_path}\\reports\\{source}_report_google.csv', sep=',', index_col=0)

    # Merge reports.
    results_merge = pd.merge(results_algorithm_selector, results_google, on='Instanz')
    results_merge = results_merge.loc[results_merge['Solver'] == 1]
    results_merge = results_merge.reset_index(drop=True)
    results_merge = results_merge.drop(columns='Instanz')
    results_merge = results_merge.rename(columns={'Makespan_x': 'Selector', 'Makespan_y': 'Google'})

    # Mark better solutions.
    results_merge['better'] = np.NaN
    for index, row in results_merge.iterrows():
        if row['Selector'] < row['Google']: results_merge['better'].iat[index] = 1
        else: results_merge['better'].iat[index] = 0

    # Number of better and worse solutions.
    better_count = sum(results_merge['better'])
    worse_count = len(results_merge) - better_count

    # Percentage of better and worse solutions.
    better = round(better_count/len(results_merge)*100,2)
    worse = round(worse_count/len(results_merge)*100,2)

    # Calculation of the result_coefficient.
    result_coefficient = round((better_count-worse_count)/len(results_merge),2)
    print('\nEvaluation Done!')


def transform_data(source, results_path):
    with open(f'{directory}\\data\\{source}_data.pkl', 'rb') as in_file:
        data = pickle.load(in_file)
    df = pd.DataFrame()
    for i in range(len(data)):
        instance = data[i]
        df = df.append({'num_jobs': len(instance.list_of_jobs),'num_machines': instance.num_machines}, ignore_index=True)
    results_meta = pd.read_csv(f'{results_path}\\reports\\{source}_report_meta.csv', sep=',', index_col=0)['Makespan']
    results_google = pd.read_csv(f'{results_path}\\reports\\{source}_report_google.csv', sep=',', index_col=0)['Makespan']
    df['meta'] = results_meta
    df['google'] = results_google
    df = df.sort_values(by=['num_jobs'])
    df = df.reset_index(drop=True)
    df['meta_better'] = np.NaN
    for index, row in df.iterrows():
        if row['meta'] < row['google']:
            df['meta_better'].iat[index] = 1
        else:
            df['meta_better'].iat[index] = 0

    df_plot = pd.DataFrame()
    df_plot = df.groupby(['num_jobs'])['meta'].mean().reset_index()
    df_plot['google'] = df.groupby(['num_jobs'])['google'].mean().reset_index()['google']
    df_plot = df_plot.rename(columns={'meta':'Metaheuristik','google':'CP-Solver'})

    return df_plot, df


# Visualisierung des Vergleichs der Metaheuristik und des CP-Solvers anhand der Test-Instanz.
def visualize_lineplot(df_plot, directory):
    df_plot_melt = df_plot.melt(id_vars=['num_jobs'], value_vars= ['Metaheuristik', 'CP-Solver'])

    fig, ax = plt.subplots(figsize=(12, 10))
    plt.title('Vergleich der Performance der Metaheuristik und des CP-Solvers', fontsize=18, pad=10)
    sns.lineplot(data=df_plot['Metaheuristik'], marker='o', sort=False, label='Metaheuristik')
    sns.lineplot(data=df_plot['CP-Solver'], marker='o', sort=False, label='CP-Solver')
    plt.vlines(x=[3, 6], ymin=1000, ymax=5200, colors='grey', ls='--', lw=2, alpha=0.7)
    plt.text(3.2, 4700, 'n = 25', rotation=90, color='grey', fontsize=12, alpha=0.8, weight="bold")
    plt.text(6.2, 4700, 'n = 40', rotation=90, color='grey', fontsize=12, alpha=0.8, weight="bold")
    plt.ylabel('makespan', fontsize=15)
    plt.xlabel('Jobanzahl', fontsize=15)
    ax.tick_params(axis='x', labelsize=10)
    ax.tick_params(axis='y', labelsize=10)
    plt.xticks(range(len(df_plot)), df_plot['num_jobs'])
    plt.legend(loc='upper left', fontsize=15)
    plt.grid(True, alpha=0.3)
    plt.show()

    fig.savefig(f'{directory}\\results\\comparison.svg', format='svg', dpi=1200)


def visualize_diff(df, directory):
    df['delta'] = df['meta'] - df['google']
    df_plot = df[['num_jobs', 'num_machines','delta']]
    df_plot["num_machines"] = df["num_machines"].apply(lambda x: f"{x} Maschinen")
    df_plot = df_plot.groupby(['num_jobs', 'num_machines'])['delta'].mean().reset_index()

    fig, ax = plt.subplots(figsize=(12, 10))
    plt.title("Differenz der Zielwerte zwischen Metaheuristik und CP-Solver", fontsize=18, pad=10)
    sns.barplot(data=df_plot, x="num_jobs", y="delta", hue="num_machines")
    plt.xlabel("Jobanzahl", fontsize=15)
    plt.ylabel("makespan Metaheuristik - makespan CP-Solver", fontsize=15)
    ax.tick_params(axis="x", labelsize=10)
    ax.tick_params(axis="y", labelsize=10)
    plt.legend(loc='upper right', fontsize=15)
    plt.grid(True, alpha=0.3)
    plt.show()

    fig.savefig(f'{directory}\\results\\comparison_diff.svg', format='svg', dpi=1200)


def visualize_boxplot(df, directory):
    df_plot = df[['num_jobs', 'num_machines', 'meta', 'google']]
    df_plot = df_plot.loc[df_plot['num_jobs'] != 100]
    df_plot = df_plot.rename(columns={'meta':'Metaheuristik','google':'CP-Solver'})
    df_plot["num_machines"] = df["num_machines"].apply(lambda x: f"{x} Maschinen")
    df_plot["num_jobs"] = df["num_jobs"].apply(lambda x: f"{x} Jobs")
    df_plot_melt = df_plot.melt(id_vars=['num_jobs', 'num_machines'], value_vars=['Metaheuristik', 'CP-Solver'])

    fig, ax = plt.subplots(figsize=(12, 5))
    plt.title("Vegleich der Ergebnisse der Instanzen mit n ≤ 50", fontsize=18, pad=10)
    sns.boxplot(data=df_plot_melt, x="value", y="variable", hue= 'num_jobs')
    plt.xlabel("makespan", fontsize=15)
    plt.ylabel("Lösungsverfahren", fontsize=15)
    ax.tick_params(axis="x", labelsize=10)
    ax.tick_params(axis="y", labelsize=10)
    plt.legend(loc='upper right', fontsize=15)
    plt.grid(True, alpha=0.3)
    plt.show()

    fig.savefig(f'{directory}\\results\\boxplot.svg', format='svg', dpi=1200)


#algorithm_selector_validation(source, directory, results_path)
df_plot, df = transform_data(source, results_path)
visualize_lineplot(df_plot, directory)
visualize_diff(df, directory)
visualize_boxplot(df, directory)
