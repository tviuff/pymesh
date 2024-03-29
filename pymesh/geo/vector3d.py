"""Module containing the Vector3D class"""

from typing import Self

import numpy as np

from pymesh.descriptors import AsInstanceOf
from pymesh.geo.point import Point
from pymesh.typing import NDArray3
from pymesh.utils import validate_move_parameters


# ! add vector math operations for easy use in the rest of the code
class Vector3D:
    """3d vector generated from two points in space"""

    start = AsInstanceOf(Point)
    end = AsInstanceOf(Point)

    def __init__(self, start: Point, end: Point) -> None:
        self.start = start
        self.end = end

    def __eq__(self, other):
        return self.start == other.start and self.end == other.end

    def __repr__(self):
        return f"{type(self).__name__}(start={self.start!r}, end={self.end!r})"

    def copy(self) -> Self:
        return Vector3D(self.start.copy(), self.end.copy())

    def move(self, dx: int | float, dy: int | float, dz: int | float) -> None:
        validate_move_parameters(dx, dy, dz)
        self.start.move(dx, dy, dz)
        self.end.move(dx, dy, dz)

    @property
    def length(self) -> float:
        return np.sqrt(np.sum((self.end - self.start) ** 2))

    @property
    def unit_vector(self) -> NDArray3[np.float64]:
        return (self.end - self.start) / self.length
