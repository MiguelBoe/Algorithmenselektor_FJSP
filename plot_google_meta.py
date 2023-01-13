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

    fig, ax = plt.subplots(figsize=(12, 10))
    plt.grid(linewidth=0.1)

    plt.bar(np.array(x_axis) + 1, machines_15, width=2)
    plt.bar(np.array(x_axis) - 1, machines_20, width=2)
    plt.rcParams["axes.linewidth"] = 0.1
    plt.title(
        "Differenz der Zielwerte zwischen CPsolver und Metaheuristik", fontsize=18
    )

    plt.xlabel("Job Anzahl", fontsize=15)
    plt.ylabel("makespan Metaheuristik - makespan CPsolver", fontsize=15)

    plt.xticks(x_axis)
    plt.yticks(np.arange(-450, 250, 50))

    plt.legend(["15 Maschinen", "20 Maschinen"], fontsize=15)

    plt.axhline(0, color="black", linewidth=1)
    ax.tick_params(axis="x", labelsize=12)
    ax.tick_params(axis="y", labelsize=12)

    fig.savefig("./diff_makespan.pdf", format="pdf", dpi=1200)
    plt.show()


if __name__ == "__main__":
    data = read_data()

    mean_meta, mean_google, data_mean = mean_data(data)

    difference = diff(mean_meta, mean_google)

    plot(difference)

