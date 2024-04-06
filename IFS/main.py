import numpy as np

from IFS.history import History
from IFS.transformation_storage import TransformationStorage


def ifs():
    transformation_storage = TransformationStorage()
    transformation_storage.from_file("data/tr1.txt")

    history = History()

    # algorithm to generate fractal
    iterations = 1000
    point = np.array([0, 0, 0])
    for _ in range(iterations):
        transformation_idx = np.random.randint(0, len(transformation_storage))
        transformation = transformation_storage[transformation_idx]
        transformed_point = transformation.transform_point(point)
        history.add(transformed_point)
        point = transformed_point

    history.animate()


if __name__ == "__main__":
    ifs()
