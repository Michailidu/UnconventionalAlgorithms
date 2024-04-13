import numpy as np
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import matplotlib.animation as animation


x_limits = (-2, 1)
y_limits = (-1, 1)


def get_values(real_values, imaginary_values):
    values = np.empty((len(real_values), len(imaginary_values)))

    for i in range(len(real_values)):
        for j in range(len(imaginary_values)):
            values[i, j] = mandelbrot(real_values[i], imaginary_values[j])

    return values.T


def mandelbrot(x, y, threshold=100):
    c = complex(x, y)
    z = complex(0, 0)
    m = 2

    for i in range(threshold):
        z = z ** 2 + c
        if abs(z) > m:
            return i

    return threshold - 1


def prepare_plot(density=500):
    x_step = (x_limits[1] - x_limits[0]) / density
    real_values = np.arange(x_limits[0], x_limits[1], x_step)
    imaginary_values = np.arange(y_limits[0], y_limits[1], x_step)

    fig = plt.gcf()
    ax = plt.gca()
    return fig, ax, (real_values, imaginary_values)


def get_animation_function(ax, real_values, imaginary_values):
    r = real_values
    i = imaginary_values

    def animate(step):
        nonlocal r, i
        global x_limits, y_limits

        if step == 0:
            x_limits = (-2, 1)
            y_limits = (-1, 1)
        print(f"Step {step}")
        ax.clear()
        ax.set_xticks([], [])
        ax.set_yticks([], [])

        zoom(ax, 0.48, 0.51, 1.1)
        _, _, (r, i) = prepare_plot()
        values = get_values(r, i)

        img = ax.imshow(values, interpolation="bicubic", cmap='plasma')
        ax.set_title(f"step: {step}")
        return [img]
    return animate


def animate_fractal():
    plt.figure(figsize=(10, 10))
    fig, ax, (real_values, imaginary_values) = prepare_plot()
    anim = animation.FuncAnimation(fig,
                                   get_animation_function(ax, real_values, imaginary_values),
                                   frames=100, interval=120, blit=True)
    anim.save('mandelbrot.gif')


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


if __name__ == '__main__':
    create_animation = True

    if create_animation:
        animate_fractal()
    else:
        interactive_mandelbrot()
