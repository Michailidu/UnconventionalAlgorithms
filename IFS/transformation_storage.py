import numpy as np

from IFS.transformation import Transformation


class TransformationStorage:
    """
    Class that stores a list of transformations
    """

    def __init__(self):
        self.transformations = []
        self.current_index = 0

    def from_file(self, file_path: str) -> None:
        """
        Load transformations from a file
        :param file_path: path to the file
        """
        with open(file_path, 'r') as file:
            for line in file:
                transformation = Transformation()
                transformation.load_from_array(np.array([float(x) for x in line.split()]))
                self.transformations.append(transformation)

    def __iter__(self):
        """
        Returns an iterator object
        """
        return iter(self.transformations)

    def __next__(self):
        """
        Returns the next transformation
        """
        if self.current_index >= len(self.transformations):
            self.current_index = 0
            raise StopIteration
        self.current_index += 1
        return self.transformations[self.current_index - 1]

    def __len__(self):
        return len(self.transformations)

    def __getitem__(self, item):
        return self.transformations[item]
