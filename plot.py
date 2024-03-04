import matplotlib
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from sklearn.metrics import accuracy_score

from geometry import LineParams, PointLimits
from perceptron import Perceptron


def categorize_predictions(df: pd.DataFrame, predictions: np.ndarray) -> pd.DataFrame:
    """
    Add a new column to the DataFrame with the categories of the predictions. Values: TP, TN, FP, FN.
    :param df: DataFrame with the dataset
    :param predictions: Numpy array with the predicted target values
    :return: DataFrame with the added column
    """
    categories = []
    true_labels = df['line_position']
    res = df.copy()
    for true_label, predicted_label in zip(true_labels, predictions):
        if true_label == 1 and predicted_label == 1:      # True Positive
            categories.append('TP')
        elif true_label == -1 and predicted_label == -1:  # True Negative
            categories.append('TN')
        elif true_label == -1 and predicted_label == 1:   # False Positive
            categories.append('FP')
        elif true_label == 1 and predicted_label == -1:   # False Negative
            categories.append('FN')
    res['category'] = categories
    return res


def plot(fig: matplotlib.figure.Figure,
         df: pd.DataFrame,
         predictions: np.ndarray,
         line_params: LineParams,
         point_limits: PointLimits,
         epoch: int = -1) -> None:
    """
    Plot the dataset and the perceptron classification.
    :param fig: Figure object to plot on
    :param df: DataFrame with the dataset
    :param predictions: Values predicted by the perceptron
    :param line_params: LineParams object with the line parameters
    :param point_limits: PointLimits object with the dataset limits
    :param epoch: Epoch number, -1 if not applicable
    :return: None
    """
    # specify the colors for the categories
    category_colors = {'TP': 'darkred',
                       'TN': 'navy',
                       'FP': 'cornflowerblue',
                       'FN': 'lightcoral'}

    # calculate the accuracy
    accuracy = accuracy_score(df['line_position'], predictions)

    # categorize the predictions
    df_cathegorized = categorize_predictions(df, predictions)

    # prepare the plot
    ax = fig.gca()
    ax.clear()
    plt.xlim(*point_limits.x_lim)
    plt.ylim(*point_limits.y_lim)

    # create legend values
    for category, color in category_colors.items():
        plt.scatter([], [], color=color, label=f'{category}', marker='o')

    # plot the dataset
    plt.scatter(df_cathegorized['x'], df_cathegorized['y'], c=df_cathegorized['category'].map(category_colors))

    # plot the line
    x_values = [0, 10]
    y_values = [line_params.a * x + line_params.b for x in x_values]
    plt.plot(x_values, y_values, color='black', linestyle='--')

    # add plot labels
    plt.xlabel('X')
    plt.ylabel('Y')
    title = f'Perceptron Classification - accuracy: {accuracy:.2f}'
    if epoch >= 0:
        title += f' - epoch: {epoch}'
    plt.title(title)
    plt.legend()
    plt.grid(True)


def make_plot(df: pd.DataFrame,
              perceptron: Perceptron,
              line_params: LineParams,
              point_limits: PointLimits) -> None:
    """
    Train the perceptron and plot the results.
    :param df: DataFrame with the dataset
    :param perceptron: Perceptron object
    :param line_params: LineParams object with the line parameters
    :param point_limits: PointLimits object with the dataset limits
    :return: None
    """
    matplotlib.use('TkAgg')

    perceptron.train(df)

    predictions = perceptron.test(df)

    fig = plt.figure(figsize=(8, 6))
    plot(fig, df, predictions, line_params, point_limits)

    plt.show()
