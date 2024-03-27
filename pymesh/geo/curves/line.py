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
        validate_length_of_line(start, end)
        self.start = start.xyz
        self.end = end.xyz

    def __eq__(self, other):
        return np.all(self.start == other.start) and np.all(self.end == other.end)

    def __ne__(self, other):
        return np.any(self.start != other.start) or np.any(self.end != other.end)

    def __repr__(self):
        txt1 = f"{type(self).__name__}("
        txt2 = f"start=Point(x={self.start[0]:.2f}, y={self.start[1]:.2f}, z={self.start[2]:.2f}), "
        txt3 = (
            f"end=Point(x={self.end[0]:.2f}, y={self.end[1]:.2f}, z={self.end[2]:.2f})"
        )
        txt4 = ")"
        return txt1 + txt2 + txt3 + txt4

    @property
    def length(self) -> float:
        return np.sqrt(np.sum((self.end - self.start) ** 2))

    def path(self, u: int | float, flip: bool = False) -> NDArray3[np.float64]:
        u = validate_curve_path_parameters(u, flip)
        return self.start + (self.end - self.start) * u

    def copy(self) -> Self:
        point0 = Point(self.start[0], self.start[1], self.start[2])
        point1 = Point(self.end[0], self.end[1], self.end[2])
        return Line(point0, point1)

    def move(
        self, dx: int | float = 0.0, dy: int | float = 0.0, dz: int | float = 0.0
    ) -> None:
        validate_move_parameters(dx, dy, dz)
        dxyz = np.array([dx, dy, dz])
        self.start += dxyz
        self.end += dxyz


def validate_length_of_line(point1: Point, point2: Point) -> None:
    """Validates line length to be non-zero"""
    if point1 == point2:
        raise ValueError("Input points must be unique")
