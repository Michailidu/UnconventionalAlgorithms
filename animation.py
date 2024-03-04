import matplotlib
import pandas as pd
from matplotlib import pyplot as plt, animation
from matplotlib.animation import FuncAnimation

from geometry import LineParams, PointLimits
from perceptron import Perceptron
from plot import plot


def animate(fig: plt.Figure,
            df: pd.DataFrame,
            perceptron: Perceptron,
            line_params: LineParams,
            point_limits: PointLimits) -> callable:
    """
    Functions for creating a callable animation function for matplotlib FuncAnimation. Callable plots each epoch of the
    perceptron algorithm.
    :param fig: Matplotlib figure object to plot on.
    :param df: DataFrame with the dataset
    :param perceptron: Perceptron object
    :param line_params: LineParams object of the dataset line parameters
    :param point_limits: PointLimits object of the dataset limits
    :return: Callable function for FuncAnimation.
    """
    def generate_frame(i):
        perceptron.train(df, max_epochs=1)
        predictions = perceptron.test(df)
        plot(fig, df, predictions, line_params, point_limits, epoch=i)
    return generate_frame


def make_animation(df: pd.DataFrame,
                   perceptron: Perceptron,
                   line_params: LineParams,
                   point_limits: PointLimits,
                   path: str = 'perceptron.gif') -> None:
    """
    Make an animation of the perceptron algorithm for the dataset and save it as a gif.
    :param df: DataFrame with the dataset
    :param perceptron: Perceptron object
    :param line_params: LineParams object of the dataset line parameters
    :param point_limits: PointLimits object of the dataset limits
    :param path: Path to save the gif
    :return:
    """
    matplotlib.use('TkAgg')
    fig = plt.figure(figsize=(8, 6))
    anim = FuncAnimation(fig, animate(fig, df, perceptron, line_params, point_limits), frames=100, interval=100)
    writer = animation.PillowWriter(fps=15,
                                    metadata=dict(artist='Me'),
                                    bitrate=1800)
    anim.save(path, writer=writer)
