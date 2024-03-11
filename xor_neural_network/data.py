import numpy as np


def generate_xor_tuple() -> np.ndarray:
    return np.round(np.random.rand(2)).astype(int)


def generate_xor_data(length: int) -> tuple[np.ndarray, np.ndarray]:
    """
    Generate XOR data and labels.
    :param length: Number of data rows to generate.
    :return: Tuple of data and labels.
    """
    data = np.array([generate_xor_tuple() for _ in range(length)])
    labels = np.logical_xor(data[:, 0], data[:, 1]).astype(int)
    return data, labels.reshape(-1, 1)


def generate_unique_xor_data() -> tuple[np.ndarray, np.ndarray]:
    """
    Generate unique XOR data and labels.
    :return: Tuple of data and labels.
    """
    data = np.array([[0, 0], [0, 1], [1, 0], [1, 1]])
    labels = np.array([[0], [1], [1], [0]])
    return data, labels
