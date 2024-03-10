from animation import make_animation
from data import generate_dataset
from geometry import PointLimits, LineParams
from perceptron import Perceptron
from plot import make_plot


def run() -> None:
    """
    Run the perceptron algorithm for randomly generated dataset and plot the results.
    :return: None
    """
    point_limits = PointLimits(x_lim=(0, 10), y_lim=(0, 10))
    line_params = LineParams(a=0.3, b=7)
    df = generate_dataset(100, point_limits, line_params)

    make_plot(df, Perceptron(), line_params, point_limits)
    # make_animation(df, Perceptron(), line_params, point_limits)


if __name__ == '__main__':
    run()
