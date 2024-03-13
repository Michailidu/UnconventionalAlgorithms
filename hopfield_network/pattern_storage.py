import numpy as np


class PatternStorage:
    def __init__(self, matrix_size: int):
        matrix_size = matrix_size ** 2
        self.weighted_matrix_sum = np.array([[0] * matrix_size] * matrix_size)

    def convert_to_pattern(self, data: np.ndarray) -> np.ndarray:
        data = data.copy()
        vector = data.reshape(-1, 1)
        vector[vector == 0] = -1
        weighted_matrix = np.matmul(vector, vector.T)
        np.fill_diagonal(weighted_matrix, 0)
        return weighted_matrix

    def add_pattern(self, pattern: np.ndarray) -> None:
        self.weighted_matrix_sum += self.convert_to_pattern(pattern)

    def remove_pattern(self, pattern: np.ndarray) -> None:
        self.weighted_matrix_sum -= self.convert_to_pattern(pattern)
