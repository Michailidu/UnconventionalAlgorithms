from matplotlib import pyplot as plt, animation

from TEA.mandelbrot import get_values
from TEA.plot import zoom, prepare_plot
from TEA.config import x_limits, y_limits


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