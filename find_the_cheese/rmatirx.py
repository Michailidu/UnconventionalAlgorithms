import numpy as np

from find_the_cheese.matrix import Matrix
from find_the_cheese.pattern_grid import PatternGrid, rewards, GridObject


class RMatrix(Matrix):
    def __init__(self, size: int):
        super().__init__(size, default_value=-1)

    def set_pattern(self, pattern_grid: PatternGrid):
        neighbors = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        for position_index in range(self.size ** 2):
            for neighbor_delta in neighbors:
                position = divmod(position_index, self.size)
                neighbor = (position[0] + neighbor_delta[0], position[1] + neighbor_delta[1])
                neighbor_index = neighbor[0] * self.size + neighbor[1]
                if 0 <= neighbor[0] < self.size and 0 <= neighbor[1] < self.size:
                    self.matrix[position_index][neighbor_index] = pattern_grid.get_reward(*neighbor)

    def choose_new_position(self, position: tuple[int, int]) -> tuple[int, int]:
        """
        Choose a new position. If a position with the cheese is found, return it. Otherwise choose randomly from the
        accessible positions.
        :param position: current position
        :return: new position
        """
        position_index = position[0] * self.size + position[1]
        if rewards[GridObject.CHEESE] in self.matrix[position_index]:
            # return position of the cheese
            return divmod(self.matrix[position_index].index(rewards[GridObject.CHEESE]), self.size)

        # choose randomly from the accessible positions
        accessible_positions = [i for i, reward in enumerate(self.matrix[position_index]) if reward != -1]
        new_position = np.random.choice(accessible_positions)
        return divmod(new_position, self.size)

    def get_best_reward(self, position: tuple[int, int]) -> int:
        """
        Get the value of the best reward of a position.
        :param position: position
        :return: best accessible reward value
        """
        position_index = position[0] * self.size + position[1]
        return max(self.matrix[position_index])

    def get_r_value(self, position_from: tuple[int, int], position_to: tuple[int, int]) -> int:
        position_from_index = position_from[0] * self.size + position_from[1]
        position_to_index = position_to[0] * self.size + position_to[1]
        return self.matrix[position_from_index][position_to_index]
