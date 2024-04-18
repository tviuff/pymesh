"""Module containing the Bezier class"""

from typing import Self

import numpy as np

from pymesh.geo.curves.curve import Curve
from pymesh.geo.point import Point
from pymesh.typing import NDArray3
from pymesh.utils import validate_curve_path_parameters


class Bezier(Curve):
    """Bezier curve generated from n points in space"""

    def __init__(self, points: list[Point]):
        self.points = points
        for point in self.points:
            if not isinstance(point, Point):
                raise TypeError(f"{point!r} is not an instance of Point")
        self.start = self.points[0]
        self.end = self.points[-1]

    def __eq__(self, other):
        is_equal = True
        if type(self).__name__ != type(other).__name__:
            is_equal = False
        else:
            for p1, p2 in zip(self.points, other.points):
                if p1 != p2:
                    is_equal = False
                    break
        return is_equal

    def __ne__(self, other):
        return not self.__eq__(other)

    def __repr__(self):
        txt = f"{type(self).__name__}(points=["
        for i, point in enumerate(self.points):
            ext = ", " if i < len(self.points) - 1 else "])"
            txt += f"{point!r}{ext}"
        return txt

    @property
    def length(self) -> float:
        raise NotImplementedError()

    def path(self, u: int | float, flip: bool = False) -> NDArray3[np.float64]:
        u = validate_curve_path_parameters(u, flip)

        def bezier(points, t):
            """Recursive bezier definition.

            Based on https://en.wikipedia.org/wiki/B%C3%A9zier_curve#Constructing_B%C3%A9zier_curves
            """
            if len(points) == 1:
                return points[0].xyz
            return (1 - t) * bezier(points[0:-1], t) + t * bezier(points[1:], t)

        return bezier(self.points, u)

    def copy(self) -> Self:
        points = []
        for point in self.points:
            points.append(point.copy())
        return Bezier(points)

    def move(
        self, dx: int | float = 0.0, dy: int | float = 0.0, dz: int | float = 0.0
    ) -> Self:
        points = []
        for point in self.points:
            points.append(point.move(dx, dy, dz))
        self.points = points
        self.start = points[0]
        self.end = points[-1]
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
