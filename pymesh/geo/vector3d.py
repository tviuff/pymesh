"""Module including line class
"""

from typing import Self

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
        return np.all(self.start == other.start) and np.all(self.end == other.end)

    def __repr__(self):
        cls = type(self).__name__
        vector = self.unit_vector * self.length
        txt = f"{cls}(dx={vector[0]:.2f}, " f"dy={vector[1]:.2f}, dz={vector[2]:.2f})"
        return txt

    def copy(self) -> Self:
        start = Point(self.start[0], self.start[1], self.start[2])
        end = Point(self.end[0], self.end[1], self.end[2])
        return Vector3D(start, end)

    def move(self, dx: int | float, dy: int | float, dz: int | float) -> None:
        for val in (dx, dy, dz):
            if not isinstance(val, (int, float)):
                raise TypeError(f"Expected {val!r} to be an int or float")
        dxyz = np.array([dx, dy, dz])
        self.start += dxyz
        self.end += dxyz

    @property
    def length(self) -> float:
        return np.sqrt(np.sum((self.end - self.start) ** 2))

    @property
    def unit_vector(self) -> NDArray3[np.float64]:
        return (self.end - self.start) / self.length
