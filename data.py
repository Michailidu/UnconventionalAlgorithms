import random

import pandas as pd

from geometry import PointLimits, LineParams


def generate_points(count: int,
                    limits: PointLimits) -> list[tuple[float, float]]:
    """
    Function to generate random points within the specified limits.
    :param count: Number of points to generate.
    :param limits: PointLimits object specifying the limits of point coordinates.
    :return: List of generated points as tuples (x, y).
    """
    points = []
    for _ in range(count):
        points.append((random.uniform(*limits.x_lim), random.uniform(*limits.y_lim)))
    return points


def evaluate_points(df: pd.DataFrame,
                    line_params: LineParams) -> pd.DataFrame:
    """
    Function to evaluate the relative position of the points to a line. Adds 'line_position' column to the DataFrame
    (0=on the line, 1=above the line, -1=below the line).
    :param df: input DataFrame with 'x' and 'y' columns.
    :param line_params: LineParams object specifying the line equation.
    :return: DataFrame with added 'line_position' column.
    """
    y_limit = df['x'] * line_params.a + line_params.b
    df['line_position'] = 1                             # Point lies above the line
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