from enum import Enum
from random import random
import matplotlib
import numpy as np

matplotlib.use('TkAgg')
import matplotlib.pyplot as plt

tree_probability = 0.05
fire_probability = 0.001
forest_density = 0.5


class Field(Enum):
    EMPTY = 0
    TREE = 1
    FIRE = 2
    ASH = 3


field_colors = {
    Field.EMPTY.value: 'white',
    Field.TREE.value: 'green',
    Field.FIRE.value: 'red',
    Field.ASH.value: 'black'
}

field_cmap = matplotlib.colors.ListedColormap([field_colors[field.value] for field in Field])


def create_grid(grid_size: int) -> list[list[Field]]:
    """
    Initialize a grid with trees and empty spaces according to the forest_density
    :param grid_size: size of the grid
    :return: new grid
    """
    return [[Field.TREE if random() < forest_density else Field.EMPTY for _ in range(grid_size)]
            for _ in range(grid_size)]


def has_burning_neighbor(grid: list[list[Field]], x: int, y: int) -> bool:
    for i in range(x - 1, x + 2):
        for j in range(y - 1, y + 2):
            if 0 <= i < len(grid) and 0 <= j < len(grid[i]) and grid[i][j] == Field.FIRE:
                return True
    return False


def update_field(grid: list[list[Field]], x: int, y: int) -> Field:
    """
    Update the field according to the rules of the forest fire model
    :param grid: the grid
    :param x: x-coordinate of the field to update
    :param y: y-coordinate of the field to update
    :return: new field value
    """
    field = grid[x][y]
    # An empty area or a burnt tree is replaced with tree_probability either by a live one or remains empty
    if field == Field.EMPTY or field == Field.ASH:
        return Field.TREE if random() < tree_probability else Field.EMPTY

    # A tree will catch fire if its neighbor is on fire
    if field == Field.TREE:
        if has_burning_neighbor(grid, x, y):
            return Field.FIRE

    # If the tree burns, it will eventually burn out and stay burned
    if field == Field.FIRE:
        return Field.ASH

    # If no tree in the neighbor is burning, then it will start burning with probability fire_probability
    return Field.FIRE if random() < fire_probability else Field.TREE


def update_grid(grid: list[list[Field]]) -> list[list[Field]]:
    new_grid = []
    for i in range(len(grid)):
        new_grid.append([])
        for j in range(len(grid[i])):
            new_grid[i].append(update_field(grid, i, j))
    return new_grid


def forest_fire(grid_size: int) -> None:
    """
    Simulate the forest fire model
    :param grid_size: size of the grid
    :return: None
    """
    grid = create_grid(grid_size)

    fig, ax = plt.subplots()

    while True:
        grid_img = np.array([[field.value for field in row] for row in grid])
        ax.imshow(grid_img, aspect='equal', cmap=field_cmap)
        plt.pause(0.01)

        grid = update_grid(grid)


if __name__ == '__main__':
    forest_fire(200)
