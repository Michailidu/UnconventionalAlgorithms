from typing import NamedTuple


class PointLimits(NamedTuple):
    """
    NamedTuple to store the limits of point coordinates.
    """
    x_lim: tuple[float, float]
    y_lim: tuple[float, float]


class LineParams(NamedTuple):
    """
    NamedTuple to store the parameters of a line equation (y = ax + b).
    """
    a: float
    b: float
