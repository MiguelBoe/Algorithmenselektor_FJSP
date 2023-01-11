import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


def read_data():
    return pd.read_csv("./df.csv")


def mean_data(data):
    data_mean = (
        data.groupby(["num_jobs", "num_machines"]).mean().drop(columns=["meta_better"])
    )
    data_mean_meta = data_mean["meta"].to_numpy()
    data_mean_google = data_mean["google"].to_numpy()

    return data_mean_meta, data_mean_google, data_mean


def diff(data_mean_meta, data_mean_google):
    return list(data_mean_meta - data_mean_google)


def plot(diff):
    machines_15 = []
    machines_20 = []
    for x in range(len(diff)):

        if (x % 2) == 0:
            machines_15.append(diff[x])
        else:
            machines_20.append(diff[x])

    x_axis = np.arange(10, 101, 5)

    plt.grid(linewidth=0.2)

    plt.bar(np.array(x_axis) + 1, machines_15, width=2)
    plt.bar(np.array(x_axis) - 1, machines_20, width=2)

    plt.title("Differenz der Zielwerte zwischen CPsolver und Metaheuristik")

    plt.xlabel("Job Anzahl")
    plt.ylabel("makespan Metaheuristik - makespan CPsolver")

    plt.xticks(x_axis)
    plt.yticks(np.arange(-450, 200, 50))

    plt.legend(["15 Maschinen", "20 Maschinen"])

    plt.axhline(0, color="black", linewidth=1)

    plt.show()


if __name__ == "__main__":
    data = read_data()

    mean_meta, mean_google, data_mean = mean_data(data)

    difference = diff(mean_meta, mean_google)

    plot(difference)

