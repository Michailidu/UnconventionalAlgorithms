import matplotlib
import numpy as np
import matplotlib.pyplot as plt


class History:
    def __init__(self):
        self.history = []

    def add(self, point: np.ndarray) -> None:
        self.history.append(point)

    def animate(self) -> None:
        """
        Create 3D animation of the history. In each step draw the next point.
        """
        matplotlib.use('TkAgg')
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        ax.set_xlim(-1, 1)
        ax.set_ylim(0, 3)
        ax.set_zlim(0, 3)

        chunk_size = 100

        for i in range(0, len(self.history), chunk_size):
            chunk = self.history[i:i + chunk_size]
            for point in chunk:
                ax.scatter(point[0], point[1], point[2], color='c')
            plt.pause(10 ** -3)

        plt.show()
