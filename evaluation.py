import pandas as pd
import numpy as np


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