import numpy as np
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt


class Plane:
    def __init__(self, points: list[float]):
        """
        Initialize 3D plane with four points
        """
        self.points = points  # rb, ru, lu, lb
        self.child_planes = []  # rb, ru, lu, lb
        self.average_height = None
        self.set_average_height()

    def set_average_height(self):
        """
        Calculate average height of the plane and set it as a class attribute
        """
        self.average_height = np.mean(self.points)

    def divide(self, height_shift: float):
        """
        Divide the plane into four smaller planes
        :param height_shift: new point has height in range [avg_height - height_shift, avg_height + height_shift]
        """
        for i in range(4):
            child_points = self.points.copy()
            new_height = self.average_height + height_shift
            child_points[(i + 1) % 4] = (new_height + child_points[(i + 1) % 4]) / 2
            child_points[(i + 2) % 4] = new_height
            child_points[(i + 3) % 4] = (new_height + child_points[(i + 3) % 4]) / 2
            self.child_planes.append(Plane(child_points))

    def create_terrain(self, level_of_detail: int, max_height_shift: float = 3):
        """
        Create a terrain with a given level of detail

        :param max_height_shift: new point has height in range
        [avg_height - max_height_shift, avg_height + max_height_shift]
        :param level_of_detail: level of detail
        """
        if level_of_detail == 0:
            return

        height_shift = 0
        if np.random.randint(0, 2):
            height_shift = np.random.uniform(-max_height_shift, max_height_shift)

        self.divide(height_shift)
        for child_plane in self.child_planes:
            child_plane.create_terrain(level_of_detail - 1, max_height_shift / 2)

    def get_height_matrix(self) -> np.ndarray:
        """
        Recursively get 2D height profile of the plane
        :return: 2D numpy array with heights
        """
        # create 2x2 matrix with heights of own points
        own_terrain = np.array([[self.points[0], self.points[1]], [self.points[3], self.points[2]]])
        if not self.child_planes:
            return own_terrain

        # get 2D height profiles of child planes
        child_terrains = [child_plane.get_height_matrix() for child_plane in self.child_planes]

        # concatenate 2D height profiles
        return np.concatenate((np.concatenate((child_terrains[0], child_terrains[1]), axis=1),
                               np.concatenate((child_terrains[3], child_terrains[2]), axis=1)), axis=0)


def plot_terrain(terrain: np.ndarray) -> None:
    """
    Create 3D plot using matplotlib of the terrain
    :param terrain: 2D numpy array with heights
    """
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    x = np.arange(terrain.shape[0])
    y = np.arange(terrain.shape[1])
    X, Y = np.meshgrid(x, y)
    Z = terrain

    ax.plot_surface(X, Y, Z, cmap='terrain')

    plt.show()


def interactive_terrain(level_of_detail: int):
    """
    Generate a terrain with a given level of detail
    :param level_of_detail: number of recursive divisions
    """
    plane = Plane([0., 0., 0., 0.])
    plane.create_terrain(level_of_detail, 1)
    terrain = plane.get_height_matrix()
    plot_terrain(terrain)


if __name__ == '__main__':
    interactive_terrain(10)
