import random

import numpy as np
import pandas as pd


class Perceptron:
    """
    Perceptron class for training and testing a simple perceptron model.
    """
    def __init__(self):
        """
        Initialize the perceptron model with random weights.
        """
        self.weights = []

        for _ in range(3):
            self.weights.append(random.uniform(0, 1))

    def train(self, df: pd.DataFrame, learning_rate: float = 0.3, max_epochs: int = 500) -> None:
        """
        Train the perceptron model on the provided DataFrame.
        :param df: DataFrame with input features and target values.
        :param learning_rate: Value specifying the learning rate of the model.
        :param max_epochs: Maximum number of epochs to train the model, if not converged.
        :return: None
        """
        epoch = 0
        converged = False
        while epoch < max_epochs and not converged:
            converged = True
            for i, row in df.iterrows():
                guess = row.iloc[0] * self.weights[0] + row.iloc[1] * self.weights[1] + self.weights[2]
                guess_signum = 1 if guess > 0 else -1
                try:
                    error = row['value'] - guess_signum
                except KeyError:
                    a = 2

                if error != 0:
                    converged = False
                    for j in range(len(self.weights)):
                        input = row.iloc[j] if j < len(df.columns) - 1 else 1
                        self.weights[j] += error * input * learning_rate

            epoch += 1

    def test(self, df: pd.DataFrame) -> np.ndarray:
        """
        Test the trained perceptron model on the provided DataFrame.
        :param df: DataFrame with input features.
        :return: Numpy array with predicted target values.
        """
        predictions = np.zeros(len(df))
        for i, row in enumerate(df.itertuples(index=False)):
            guess = row[0] * self.weights[0] + row[1] * self.weights[1] + self.weights[2]
            predictions[i] = 1 if guess > 0 else -1
        return predictions
