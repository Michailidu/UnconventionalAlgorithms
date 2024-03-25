import numpy as np

from find_the_cheese.matrix import Matrix


class QMatrix(Matrix):
    def __init__(self, size: int):
        super().__init__(size, default_value=0)

    def reset(self) -> None:
        self.matrix = np.zeros((self.size ** 2, self.size ** 2))

    def get_q_value(self, position_from: tuple[int, int], position_to: tuple[int, int]) -> float:
        position_from_index = position_from[0] * self.size + position_from[1]
        position_to_index = position_to[0] * self.size + position_to[1]
        return self.matrix[position_from_index, position_to_index]

    def set_q_value(self, position_from: tuple[int, int], position_to: tuple[int, int], value: float) -> None:
        position_from_index = position_from[0] * self.size + position_from[1]
        position_to_index = position_to[0] * self.size + position_to[1]
        self.matrix[position_from_index, position_to_index] = value

    def get_best_new_position(self, position: tuple[int, int]) -> tuple[int, int]:
        """
        Move to the best position from the current position. If there are multiple best positions, choose randomly.
        :param position: current position
        :return: best position
        """
        position_index = position[0] * self.size + position[1]
        best_positions = np.where(self.matrix[position_index] == np.max(self.matrix[position_index]))[0]
        return divmod(np.random.choice(best_positions), self.size)

    def get_best_q_value(self, position: tuple[int, int]) -> float:
        """
        Get the value of the best reward of a position.
        :param position: position
        :return: best accessible reward value
        """
        position_index = position[0] * self.size + position[1]
        return np.max(self.matrix[position_index])
