import numpy as np


class Transformation:
    """
    Class that represents affine transformation in 3D space
    """
    def __init__(self):
        """
        Initialize with identity transformation
        """
        self.rotation_scale_matrix = np.array([[1, 0, 0], [0, 1, 0], [0, 0, 1]])
        self.translation_matrix = np.array([0, 0, 0])

    def load_from_array(self, array: np.ndarray) -> None:
        """
        Load transformation from 1D numpy array
        :param array: 1D numpy array
        """
        self.rotation_scale_matrix = array[:9].reshape((3, 3))
        self.translation_matrix = array[9:]

    def transform_point(self, point: np.ndarray) -> np.ndarray:
        """
        Apply transformation to a point and return new point
        :param point: 1D numpy array with 3 elements
        :return: transformed point
        """
        return np.dot(self.rotation_scale_matrix, point) + self.translation_matrix
