class Matrix:
    def __init__(self, size: int, default_value: int):
        self.size = size
        self.matrix = [[default_value for _ in range(size ** 2)] for _ in range(size ** 2)]

    def get_neighbor_values(self, position: tuple[int, int]) -> list[int]:
        neighbors = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        values = []
        position_index = position[0] * self.size + position[1]
        for neighbor_delta in neighbors:
            neighbor = (position[0] + neighbor_delta[0], position[1] + neighbor_delta[1])
            if 0 <= neighbor[0] < self.size and 0 <= neighbor[1] < self.size:
                neighbor_index = neighbor[0] * self.size + neighbor[1]
                values.append(self.matrix[position_index][neighbor_index])
            else:
                values.append(None)
        return values
