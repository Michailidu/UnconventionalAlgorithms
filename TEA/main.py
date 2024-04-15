import matplotlib

from TEA.animation import animate_fractal
from TEA.plot import interactive_mandelbrot

matplotlib.use('TkAgg')


if __name__ == '__main__':
    create_animation = False

    if create_animation:
        animate_fractal()
    else:
        interactive_mandelbrot()
