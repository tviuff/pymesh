"""Module including line class
"""

import numpy as np

from pymesh.geo.point import Point
from pymesh.typing import NDArray3
from pymesh.descriptors import AsNDArray

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
        cls = type(self).__name__
        vector = self.unit_vector * self.length
        txt = f"{cls}(dx={vector[0]:.2f}, " f"dy={vector[1]:.2f}, dz={vector[1]:.2f})"
        return txt

    @property
    def length(self) -> float:
        return np.sqrt(np.sum((self.end - self.start) ** 2))

    @property
    def unit_vector(self) -> NDArray3[np.float64]:
        return (self.end - self.start) / self.length
