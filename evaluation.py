import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pickle
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

# Konfigurationsbereich.
#----------------------------------------------------------------------------------------------------------------------#
results_path = '\\Users\\migue\\PycharmProjects\\Algorithmenselektor_JSP\\results'
source = 'test'
#----------------------------------------------------------------------------------------------------------------------#


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
print('Done!')


def visualize_it(source, results_path):
    with open(f'\\Users\\migue\\PycharmProjects\\Algorithmenselektor_JSP\\data\\{source}_data.pkl', 'rb') as in_file:
        data = pickle.load(in_file)
    df = pd.DataFrame()
    for i in range(len(data)):
        instance = data[i]
        df = df.append({'num_jobs': len(instance.list_of_jobs),'num_machines': instance.num_machines}, ignore_index=True)
    results_meta = pd.read_csv(f'{results_path}\\reports\\{source}_report_meta.csv', sep=',', index_col=0)[
        'Makespan']
    results_google = pd.read_csv(f'{results_path}\\reports\\{source}_report_google.csv', sep=',', index_col=0)[
        'Makespan']
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

    df_bar = pd.DataFrame()
    df_bar = df.groupby(['num_jobs'])['meta'].mean().reset_index()
    df_bar['google'] = df.groupby(['num_jobs'])['google'].mean().reset_index()['google']
    df_bar = df_bar.rename(columns={'meta':'Metaheuristik','google':'CP-Solver'})

    df_bar_melt = df_bar.melt(id_vars=['num_jobs'], value_vars= ['Metaheuristik', 'CP-Solver'])

    fig, ax = plt.subplots(figsize=(12, 10))
    plt.title('Vergleich der Performance der Metaheuristik und des CP-Solvers', fontsize=18, pad=20)
    sns.barplot(data=df_bar_melt, x="num_jobs", y="value", hue="variable", ax=ax)
    sns.lineplot(data=df_bar['Metaheuristik'], marker='o', sort=False, ax=ax)
    sns.lineplot(data=df_bar['CP-Solver'], marker='o', sort=False, ax=ax)
    ax.vlines(x=[3, 6], ymin=0, ymax=5600, colors='grey', ls='--', lw=2, alpha=0.7)
    plt.text(3.2, 5000, 'n = 25', rotation=90, color='grey', fontsize=12, alpha=0.8, weight="bold")
    plt.text(6.2, 5000, 'n = 40', rotation=90, color='grey', fontsize=12, alpha=0.8, weight="bold")
    plt.ylabel('makespan', fontsize=15)
    plt.xlabel('Anzahl Jobs n', fontsize=15)
    ax.tick_params(axis='x', labelsize=10)
    ax.tick_params(axis='y', labelsize=10)
    plt.legend( loc='upper left', fontsize=10)
    plt.show()
    fig.savefig('\\Users\\migue\\Desktop\\comparison.svg', format='svg', dpi=1200)

    print()

visualize_it(source, results_path)
