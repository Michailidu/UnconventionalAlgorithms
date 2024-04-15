import numpy as np
from matplotlib import pyplot as plt

from TEA.mandelbrot import get_values
from TEA.config import x_limits, y_limits


def prepare_plot(density=500):
    x_step = (x_limits[1] - x_limits[0]) / density
    real_values = np.arange(x_limits[0], x_limits[1], x_step)
    imaginary_values = np.arange(y_limits[0], y_limits[1], x_step)

    fig = plt.gcf()
    ax = plt.gca()
    return fig, ax, (real_values, imaginary_values)


def zoom(ax, x, y, zoom_ratio=2.):
    global x_limits, y_limits
    xmin_win, xmax_win = ax.get_xlim()
    if xmin_win > xmax_win:
        xmin_win, xmax_win = xmax_win, xmin_win
    ymax_win, ymin_win = ax.get_ylim()
    if ymin_win > ymax_win:
        ymin_win, ymax_win = ymax_win, ymin_win

    x_range = x_limits[1] - x_limits[0]
    y_range = y_limits[1] - y_limits[0]

    x_rat = (x - xmin_win) / (xmax_win - xmin_win)
    y_rat = (y - ymin_win) / (ymax_win - ymin_win)

    x_pos = x_rat * x_range + x_limits[0]
    y_pos = y_rat * y_range + y_limits[0]

    x_min = x_pos - x_range / (2 * zoom_ratio)
    y_min = y_pos - y_range / (2 * zoom_ratio)
    x_max = x_pos + x_range / (2 * zoom_ratio)
    y_max = y_pos + y_range / (2 * zoom_ratio)

    x_limits = (x_min, x_max)
    y_limits = (y_min, y_max)


def on_click(event, ax):
    global x_limits, y_limits
    if event.button == 1:  # Left mouse button
        x_win, y_win = event.xdata, event.ydata
        zoom(ax, x_win, y_win)
        interactive_mandelbrot()


def interactive_mandelbrot(density=500):
    fig, ax, (real_values, imaginary_values) = prepare_plot(density)
    values = get_values(real_values, imaginary_values)

    fig.canvas.mpl_connect('button_press_event', lambda event: on_click(event, ax))
    ax.imshow(values, interpolation="bicubic", cmap='plasma')
    plt.show()
