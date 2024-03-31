"""Module containing the Vector3D class"""

from typing import Self

import numpy as np

from pymesh.descriptors import AsInstanceOf
from pymesh.geo.point import Point
from pymesh.typing import NDArray3


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
        """Returns a copy of vector instance"""
        return Vector3D(self.start.copy(), self.end.copy())

    def move(self, dx: int | float, dy: int | float, dz: int | float) -> Self:
        self.start.move(dx, dy, dz)
        self.end.move(dx, dy, dz)
        return self

    def rotate(
        self,
        angle: int | float,
        a: int | float,
        b: int | float,
        c: int | float,
        x0: int | float = 0.0,
        y0: int | float = 0.0,
        z0: int | float = 0.0,
    ) -> Self:
        self.start.rotate(angle, a, b, c, x0, y0, z0)
        self.end.rotate(angle, a, b, c, x0, y0, z0)
        return self

    def mirror(
        self,
        a: int | float,
        b: int | float,
        c: int | float,
        x0: int | float = 0.0,
        y0: int | float = 0.0,
        z0: int | float = 0.0,
    ) -> Self:
        """Mirrors vector in a plane.

        Plane is defined by a normal vector (a, b, c) and a point (x0, y0, z0).
        By default x0 = 0.0, y0 = 0.0 and z0 = 0.0.
        """
        self.start.mirror(a, b, c, x0, y0, z0)
        self.end.mirror(a, b, c, x0, y0, z0)
        return self

    @property
    def length(self) -> float:
        return np.sqrt(np.sum((self.end - self.start) ** 2))

    @property
    def unit_vector(self) -> NDArray3[np.float64]:
        return (self.end - self.start) / self.length
