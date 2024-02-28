import numpy as np
import pandas as pd
import random
from typing import NamedTuple
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score


class PointLimits(NamedTuple):
    x_lim: tuple[float, float]
    y_lim: tuple[float, float]


class LineParams(NamedTuple):
    a: float
    b: float


def generate_points(count: int,
                    limits: PointLimits) -> list[tuple[float, float]]:
    points = []
    for _ in range(count):
        points.append((random.uniform(*limits.x_lim), random.uniform(*limits.y_lim)))
    return points


def evaluate_points(df: pd.DataFrame, line_params: LineParams) -> pd.DataFrame:
    y_limit = df['x'] * line_params.a + line_params.b
    df['line_position'] = 0                             # Point lies on the line
    df.loc[df['y'] > y_limit, 'line_position'] = 1      # Point lies above the line
    df.loc[df['y'] < y_limit, 'line_position'] = -1     # Point lies below the line
    return df


def generate_dataset(count: int,
                     limits: PointLimits,
                     line_params: LineParams) -> pd.DataFrame:
    """
    Function to generate random point dataset with the following columns:
    x: x position of a point,
    y: y position of a point,
    line_position: relative position of the point to a line (0=on the line, 1=above the line, -1=below the line).

    :param count: Number of points to generate.
    :param limits: PointLimits object specifying the limits of point coordinates.
    :param line_params: LineParams object specifying the line equation.
    :return: DataFrame of the generated points.
    """
    df = pd.DataFrame(generate_points(count, limits), columns=['x', 'y'])
    df = evaluate_points(df, line_params)
    return df


class Perceptron:
    def __init__(self):
        self.weights = []

    def train(self, df: pd.DataFrame, learning_rate: float = 0.1, max_epochs: int = 1000):
        for _ in range(len(df.columns)):
            self.weights.append(random.uniform(0, 1))

        epoch = 0
        converged = False
        while epoch < max_epochs and not converged:
            converged = True
            for i, row in df.iterrows():
                guess = row[0] * self.weights[0] + row[1] * self.weights[1] + self.weights[2]
                guess_signum = 1 if guess > 0 else -1
                error = row['line_position'] - guess_signum

                if error != 0:
                    converged = False
                    for j in range(len(self.weights)):
                        input = row[j] if j < len(df) - 1 else 1
                        self.weights[j] += error * input * learning_rate

            epoch += 1

    def test(self, df: pd.DataFrame) -> np.ndarray:
        predictions = np.zeros(len(df))
        for i, row in enumerate(df.itertuples(index=False)):
            guess = row[0] * self.weights[0] + row[1] * self.weights[1] + self.weights[2]
            predictions[i] = 1 if guess > 0 else -1
        return predictions


if __name__ == '__main__':
    point_limits = PointLimits(x_lim=(0, 10), y_lim=(0, 10))
    line_params = LineParams(a=2, b=3)
    df = generate_dataset(100, point_limits, line_params)

    train_df, test_df = train_test_split(df, test_size=0.2, random_state=16)

    perceptron = Perceptron()
    perceptron.train(train_df)

    train_predictions = perceptron.test(train_df)
    test_predictions = perceptron.test(test_df)

    train_accuracy = accuracy_score(train_df['line_position'], train_predictions)
    test_accuracy = accuracy_score(test_df['line_position'], test_predictions)

    print("train accuracy:", train_accuracy)
    print("test accuracy:", test_accuracy)
