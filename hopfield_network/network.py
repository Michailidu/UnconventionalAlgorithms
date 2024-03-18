import numpy as np

from hopfield_network.pattern_storage import PatternStorage


class HopfieldNetwork:
    """
    Class to store patterns and recover them using a Hopfield network
    """
    def __init__(self, matrix_size: int):
        self.weighted_matrix = PatternStorage(matrix_size)
        self.patterns = []

    def add_pattern(self, pattern: np.array) -> np.array:
        self.weighted_matrix.add_pattern(pattern)
        self.patterns.append(pattern.copy())
        return pattern

    def remove_pattern(self, pattern: np.array) -> np.array:
        self.weighted_matrix.remove_pattern(pattern)
        for idx, stored_pattern in enumerate(self.patterns):
            if np.array_equal(stored_pattern, pattern):
                self.patterns.pop(idx)
                break
        return pattern

    def remove_all_patterns(self) -> np.array:
        self.weighted_matrix.weighted_matrix_sum = np.zeros_like(self.weighted_matrix.weighted_matrix_sum)
        self.patterns = []
        return np.zeros_like(self.weighted_matrix.weighted_matrix_sum)

    def recover_sync(self, pattern: np.array) -> np.array:
        """
        Method to recover a pattern using synchronous algorithm
        :param pattern: Current pattern to recover
        :return: Recovered pattern
        """
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
        """
        Method to recover a pattern using asynchronous algorithm
        :param pattern: Current pattern to recover
        :return: Recovered pattern
        """
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

    def get_all_patterns(self) -> list:
        return self.patterns
