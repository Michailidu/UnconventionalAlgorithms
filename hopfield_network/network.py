import numpy as np

from hopfield_network.pattern_storage import PatternStorage


class HopfieldNetwork:
    def __init__(self, matrix_size: int):
        self.weighted_matrix = PatternStorage(matrix_size)

    def add_pattern(self, pattern: np.array) -> None:
        self.weighted_matrix.add_pattern(pattern)

    def remove_pattern(self, pattern: np.array) -> None:
        self.weighted_matrix.remove_pattern(pattern)

    def remove_all_patterns(self) -> None:
        self.weighted_matrix.weighted_matrix_sum = np.zeros_like(self.weighted_matrix.weighted_matrix_sum)

    def recover_sync(self, pattern: np.array) -> np.array:
        pattern = pattern.copy()
        size = pattern.shape[0]
        pattern = pattern.reshape(-1, 1)
        pattern[pattern == 0] = -1
        for _ in range(10):
            pattern = np.sign(np.dot(self.weighted_matrix.weighted_matrix_sum, pattern))
        pattern = pattern.reshape(size, size)
        pattern[pattern == -1] = 0
        return pattern

    def recover_async(self, pattern: np.array) -> np.array:
        pattern = pattern.copy()
        size = pattern.shape[0]
        pattern = pattern.reshape(-1, 1)
        pattern[pattern == 0] = -1
        for _ in range(20):
            for i in range(size):
                neuron_sum = np.dot(self.weighted_matrix.weighted_matrix_sum[i], pattern)
                pattern[i] = np.sign(neuron_sum)
        pattern = pattern.reshape(size, size)
        pattern[pattern == -1] = 0
        return pattern
