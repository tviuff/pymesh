from typing import Self

import numpy as np

from pymesh.geo.curves.curve import Curve
from pymesh.geo.point import Point
from pymesh.typing import NDArray3
from pymesh.utils import validate_curve_path_parameters


class Line(Curve):
    """Creates a straight line object, generated from two points in space.

    For more information, see Curve documentation.
    """

    def __init__(self, start: Point, end: Point):
        """Initialization method.

        Args:
            start (Point): Line start point
            end (Point): Line end point

        Raises:
            ValueError: If start and end points are the same.
        """
        self.start = start
        self.end = end
        if start == end:
            raise ValueError("start and end points are the same")

    def __eq__(self, other):
        return self.start == other.start and self.end == other.end

    def __ne__(self, other):
        return not self.__eq__(other)

    def __repr__(self):
        return f"{type(self).__name__}(start={self.start!r}, end={self.end!r})"

    @property
    def length(self) -> float:
        return np.sqrt(np.sum((self.end - self.start) ** 2))

    def path(self, u: int | float, flip: bool = False) -> NDArray3[np.float64]:
        u = validate_curve_path_parameters(u, flip)
        return self.start.xyz + (self.end - self.start) * u

    def copy(self) -> Self:
        return Line(self.start.copy(), self.end.copy())

    def move(
        self, dx: int | float = 0.0, dy: int | float = 0.0, dz: int | float = 0.0
    ) -> Self:
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
        self.start.mirror(a, b, c, x0, y0, z0)
        self.end.mirror(a, b, c, x0, y0, z0)
        return self
