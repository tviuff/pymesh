"""Module including line class
"""

from typing import Self

import numpy as np

from pymesh.geo.curves.curve import Curve
from pymesh.geo.point import Point
from pymesh.typing import NDArray3
from pymesh.utils import validate_move_parameters, validate_curve_path_parameters


class Line(Curve):
    """Line generated from two points in space"""

    def __init__(self, start: Point, end: Point):
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
    ) -> None:
        validate_move_parameters(dx, dy, dz)
        self.start.move(dx, dy, dz)
        self.end.move(dx, dy, dz)
