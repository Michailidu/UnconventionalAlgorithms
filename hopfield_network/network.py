import numpy as np

from hopfield_network.pattern_storage import PatternStorage


class HopfieldNetwork:
    def __init__(self, matrix_size: int):
        self.weighted_matrix = PatternStorage(matrix_size)

    def add_pattern(self, pattern: np.array) -> np.array:
        self.weighted_matrix.add_pattern(pattern)
        return pattern

    def remove_pattern(self, pattern: np.array) -> np.array:
        self.weighted_matrix.remove_pattern(pattern)
        return pattern

    def remove_all_patterns(self) -> np.array:
        self.weighted_matrix.weighted_matrix_sum = np.zeros_like(self.weighted_matrix.weighted_matrix_sum)
        return np.zeros_like(self.weighted_matrix.weighted_matrix_sum)

    def recover_sync(self, pattern: np.array) -> np.array:
        pattern = pattern.copy()
        size = pattern.shape[0]
        pattern = pattern.reshape(-1, 1)
        pattern[pattern == 0] = -1
        for _ in range(20):
            pattern = np.sign(np.dot(self.weighted_matrix.weighted_matrix_sum, pattern))
        pattern = pattern.reshape(size, size)
        pattern[pattern == -1] = 0
        return pattern

    def recover_async(self, pattern: np.array) -> np.array:
        pattern = pattern.copy()
        size = pattern.shape[0]
        pattern = pattern.reshape(1, -1)
        pattern[pattern == 0] = -1
        for _ in range(20):
            for i in range(0, size * size):
                matrix_column = self.weighted_matrix.weighted_matrix_sum[:, i].reshape(1, -1)
                neuron_sum = np.dot(pattern, matrix_column.T)
                pattern[0, i] = 1 if neuron_sum[0, 0] >= 0 else 0
        pattern = pattern.reshape(size, size)
        pattern[pattern == -1] = 0
        return pattern
