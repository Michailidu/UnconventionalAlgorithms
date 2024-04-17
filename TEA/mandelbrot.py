import numpy as np


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
