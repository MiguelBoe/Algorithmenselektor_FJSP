from __future__ import absolute_import, division, print_function, unicode_literals
import pickle
import tensorflow as tf
import matplotlib.pyplot as plt
import numpy as np
import time
import pandas as pd
import sys
from sklearn.metrics import f1_score
from sklearn.model_selection import train_test_split

start = time.time()


def read_data():
    """
    input_KNN : DataFrame
        Inputdaten für das KNN.
    output : DataFrame
        Outputdaten für das KNN.
    """

    with open(f"train_set.pkl", "rb") as in_file:
        train_data = pickle.load(in_file)
    # with open(f"train_data.pkl", "rb") as in_file:
    #     train_data = pickle.load(in_file)

    input_data = train_data.iloc[:, :-1]
    output_data = train_data.iloc[:, -1].to_numpy()

    input_train, input_test, output_train, output_test = train_test_split(
        input_data, output_data, test_size=0.2, shuffle=True, random_state=3
    )

    print(input_train, input_test, output_train, output_test)
    return input_train, input_test, output_train, output_test


def model_konf(input_train, output_train):
    """
    Konfiguration des Tensorflow-Modells.
    Hier wird das künstliche neuronale Netz 
    erstellt, seine Layer und deren Aktivierungsfunktionen definiert und der Optimizer 
    (adam) festgelegt. 

    Returns
    -------
    model : keras.engine.sequential.Sequential
        Das konfigurierte Modell.

    """
    # Dimension des Inputs (Jahr, Monat, Tag, Stunde) und somit Anzahl der künstlichen Neuronen im Inputlayer.
    Nin = np.shape(input_train)[1]

    # model definieren
    model = tf.keras.Sequential()

    # model anpassen
    # Definieren der Anzahl der Layer, Anzahl der Neuronen im Layer, Aktivierungsfunktionen
    model.add(tf.keras.layers.InputLayer(input_shape=Nin))
    model.add(tf.keras.layers.Dense(75, activation="relu"))
    # model.add(tf.keras.layers.Dense(50, activation="relu"))
    # model.add(tf.keras.layers.Dense(25, activation="relu"))
    # model.add(tf.keras.layers.Dense(10, activation="relu"))
    model.add(tf.keras.layers.Dense(2, activation="softmax"))

    # Modell kompilieren
    model.compile(
        optimizer="rmsprop",
        loss="sparse_categorical_crossentropy",
        metrics=["accuracy"],
    )
    # Modell als Übersicht ausgeben
    model.summary()

    return model


def model_train(model, x, y):
    """
    Trainieren des vorher konfigurierten Modell.

    Parameters
    ----------
    model : keras.engine.sequential.Sequential
        Das konfigurierte Modell.
    x : Array
        Inputdaten für das KNN.
    y : DataFrame
        Entsprechende Outputdaten.

    Returns
    -------
    history: keras.callbacks.History
        Speichert den Loss und die Accuracy ab.
        Sowohl für Trainingsdaten als auch für die Validierungdaten.

    """
    return model.fit(x, y, epochs=2000, batch_size=50, verbose=1, validation_split=0.1)


def save_model(model):

    path_model = "../model"

    model.save(path_model)
    return


def model_test(model, input_test, output_test):
    """
    Testen des trainierten KNNs anhand der Test-Daten

    Parameters
    ----------
    model : keras.engine.sequential.Sequential
        Das konfigurierte Modell.
    
       
    Returns
    -------

    predictions_x_test : DataFrame
        Vorhersage für den Output auf Grundlage der Daten von x_test.
        
    predictions_with_input : DataFrame
        Vorhersage mit Inputdaten zusammengeführt.

    """

    predictions_x_test = pd.DataFrame(model.predict(input_test))

    predictions_with_input = pd.DataFrame(np.c_[input_test, predictions_x_test])

    return predictions_x_test, predictions_with_input


def data_hist(output_test, predictions):
    """
    Daten zum Vergleich der Vorhersagewerte und den tatsächlichen Werten.

    Parameters
    ----------
    y_test : DataFrame
        Tatsächliche Werte.
    predictions : DataFrame
        Vorhergesagte Werte.

    Returns
    -------
    diff : array
        Differenzen zwischen der Vorhersage und den tatsächlichen Werten.

    """

    predictions = np.array(predictions)
    # output_test = output_test.to_numpy()
    diff = [
        (np.argmax(predictions[i])) - output_test[i] for i in range(len(output_test))
    ]

    diff = np.array(diff)

    unique, counts = np.unique(diff, return_counts=True)

    for u, c in zip(unique, counts):
        print(f"# {u} : {c}")
    print("------------------------------------------------")
    return diff


"""
Darstellung der Ergebnisse
"""


def plots(history, diff):

    # Accuracy und Loss
    fig1, ax1 = plt.subplots(2, 1, sharex=True, figsize=(17, 10))
    ax1[0].grid()
    ax1[1].grid()
    plt.xlabel("Epochen", fontsize=18)
    ax1[0].tick_params(axis="both", which="major", labelsize=18)
    ax1[0].tick_params(axis="both", which="minor", labelsize=18)
    ax1[1].tick_params(axis="both", which="major", labelsize=18)
    ax1[1].tick_params(axis="both", which="minor", labelsize=18)
    ax1[0].plot(history.history["loss"], linewidth=3)
    ax1[0].set_ylabel("Loss", fontsize=18)
    ax1[1].plot(history.history["accuracy"], linewidth=3)
    ax1[1].set_ylabel("Accuracy", fontsize=18)

    # hist
    fig2, ax2 = plt.subplots(1, 1, sharex=True, figsize=(17, 10))
    ax2.set_xticks([-5, -4, -3, -2, -1, 0, 1, 2, 3, 4])
    ax2.tick_params(axis="both", which="major", labelsize=18)
    ax2.tick_params(axis="both", which="minor", labelsize=18)
    plt.xlabel("Differenz zur tatsächlichen Unfallanzahl", fontsize=18)
    plt.ylabel("Anzahl", fontsize=18)
    ax2.hist(
        diff, bins=[-5, -4.5, -4, -3.5, -2.5, -1.5, -0.5, 0.5, 1.5, 2.5, 3.5, 4, 4.5]
    )
    plt.show()

    # val acc
    fig3, ax3 = plt.subplots(2, 1, sharex=True, figsize=(17, 10))
    ax3[0].grid()
    ax3[1].grid()
    plt.xlabel("Epochen", fontsize=18)
    ax3[0].tick_params(axis="both", which="major", labelsize=18)
    ax3[0].tick_params(axis="both", which="minor", labelsize=18)
    ax3[1].tick_params(axis="both", which="major", labelsize=18)
    ax3[1].tick_params(axis="both", which="minor", labelsize=18)
    ax3[0].plot(history.history["val_loss"], linewidth=3)
    ax3[0].set_ylabel("validation Loss", fontsize=10)
    ax3[1].plot(history.history["val_accuracy"], linewidth=3)
    ax3[1].set_ylabel("validation Accuracy", fontsize=10)

    return


if __name__ == "__main__":
    # Einlesen der Daten
    input_train, input_test, output_train, output_test = read_data()

    # Konfigurieren des Modells

    model_num = model_konf(input_train, output_train)

    # Trainieren des Modells
    history_num = model_train(model_num, input_train, output_train)

    # Abspeichern des trainierten Modells
    save_model(model_num)

    # Testen des trainierten Modells
    predictions_y, predictions_with_input = model_test(
        model_num, input_test, output_test
    )

    # Vergleichen der Vorhersage zu den tatsächlichen Wertem
    diff = data_hist(output_test, predictions_y)

    # Plotten der Ergebnisse
    plots(history_num, diff)

    end = time.time()
    print(f"time : {end - start}")

