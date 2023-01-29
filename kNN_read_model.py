"""
@author: böttcher & pretz

#-----------------------------------------------------------------------------#
#         Projektseminar Business Analytics - Wintersemester 22/23            #
#-----------------------------------------------------------------------------#
#                                                                             #
#             Evaluation und Vorhesage des Abgespeicherten KNNs               #
#                                                                             # 
#                                                                             #
#-----------------------------------------------------------------------------#
"""

from __future__ import absolute_import, division, print_function, unicode_literals
import numpy as np
import pandas as pd
from pandas import read_csv
import keras


def read_model_data(data: pd.DataFrame, attribute: str):
    "Aufteilen der Daten in INput und Output und einlesen des Modells"

    model = keras.models.load_model(f"model_{attribute}_attribute_knn")

    # je nach Attribut Anzahl werden andere Daten benötigt
    if attribute == "all":
        input_test = data.iloc[1:, 1:-1].to_numpy(dtype=float)
    elif attribute == "1_5":
        input_test = data.iloc[1:, 1:6].to_numpy(dtype=float)
    elif attribute == "1_6":
        input_test = data.iloc[1:, 1:17].to_numpy(dtype=float)
    elif attribute == "1":
        input_test = data.iloc[1:, 2:3].to_numpy(dtype=float)

    # Outputdaten -> nur zum Evaluieren wichtig
    output_test = data.iloc[1:, -1].to_numpy(dtype=float)
    output_test = np.reshape(output_test, (len(output_test), 1))

    return input_test, output_test, model


def evaluate(read_model_data, attribute):
    # Testdatensatz der Evaluiert werden soll
    path = ".//data//test_von_train.csv"
    data = read_csv(path, header=None)
    input_test, output_test, model = read_model_data(data, attribute)

    results = model.evaluate(input_test, output_test)
    print("-----------------------------------------------------------------------------")
    print(f"Auf diesen Testdatensatz wurde eine Accuracy-Score von {results[1]} erreicht")
    print("-----------------------------------------------------------------------------")


def predict(read_model_data, attribute):
    path = ".//data//test_set.csv"
    data = read_csv(path, header=None)
    input_test, _, model = read_model_data(data, attribute)

    predictions = model.predict(input_test)
    predictions = pd.DataFrame(predictions, columns=["0", "1"])
    predictions.to_csv("predictions_KNN.csv", index=False)

    print("----------------------------------------------------------------------------------")
    print("Für die eingelesenen Inputdaten wurde eine Vorhersage generiert und abgespechert")
    print("----------------------------------------------------------------------------------")


if __name__ == "__main__":

    # Angabe ob das model evaluiert werden soll oder eine Vorhersage treffen soll
    mode = "predict"  # predict, evaluate

    # Auswahl des modells, welches evaluiert werden soll
    # Alle attribute, 1 bis 5, 1 bis 6 oder nur Anzahl der Jobs
    attribute = "1"  # 'all', '1_5', '1_6', 1

    if mode == "evaluate":
        evaluate(read_model_data, attribute)

    else:
        predict(read_model_data, attribute)

