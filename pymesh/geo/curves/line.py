"""Module including line class
"""

import numpy as np

from pymesh.geo.point import Point
from pymesh.geo.curves.curve import (
    Curve,
    validate_curve_path_parameters,
)
from pymesh.utils.typing import NDArray3


def validate_length_of_line(point1: Point, point2: Point) -> None:
    """Validates line length to be non-zero"""
    if point1 == point2:
        raise ValueError("Input points must be unique")


class Line(Curve):
    """Line generated from two points in space"""

    def __init__(self, start: Point, end: Point):
        validate_length_of_line(start, end)
        self.start = start.xyz
        self.end = end.xyz

    def __eq__(self, other):
        return np.all(self.start == other.start) and np.all(self.end == other.end)

    def __repr__(self):
        txt = (
            f"{type(self).__name__}(",
            f"Point({self.start[0]}, {self.start[1]}, {self.start[2]}), ",
            f"Point({self.end[0]}, {self.end[1]}, {self.end[2]})",
            ")",
        )
        return txt[0]

    @property
    def length(self) -> float:
        return np.sqrt(np.sum((self.end - self.start) ** 2))

    def path(self, u: int | float, flip: bool = False) -> NDArray3[np.float64]:
        u = validate_curve_path_parameters(u, flip)
        return self.start + (self.end - self.start) * u
