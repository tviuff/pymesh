"""Module including line class
"""

import numpy as np
from numpy import ndarray

from pygdf.auxiliary.point import Point
from pygdf.descriptors import AsNDArray

# ! add vector math operations for easy use in the rest of the code


class Vector3D:
    """3d vector generated from two points in space"""

    start = AsNDArray(shape=(3,))
    end = AsNDArray(shape=(3,))

    def __init__(self, start: Point, end: Point) -> None:
        self.start = start.xyz
        self.end = end.xyz

    def __eq__(self, other):
        return (
            np.all(self.unit_vector == other.unit_vector)
            and self.length == other.length
        )

    def __repr__(self):
        # ! does not work properly
        cls = type(self).__name__
        vector = self.unit_vector * self.length
        txt = f"{cls}(dx={vector[0]}, " f"dy={vector[1]}, dz={vector[1]})"
        return txt

    @property
    def length(self) -> float:
        return np.sqrt(np.sum((self.end - self.start) ** 2))

    @property
    def unit_vector(self) -> ndarray:
        return (self.end - self.start) / self.length
