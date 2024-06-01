"""Module containing the Bezier class"""

from typing import Self

import numpy as np

from pymesh.geo.curves.curve import Curve
from pymesh.geo.point import Point
from pymesh.typing import NDArray3
from pymesh.descriptors import AsContainerOf
from pymesh.utils import validate_curve_path_parameters

NUM_POINTS = 1000


class Bezier(Curve):
    """Creates a bezier curve from a collection of three-dimensional points.

    Attributes:
        points (list[Point] | tuple[Point]): List or tuple of points.
    """

    points = AsContainerOf(tuple, Point, min_length=2)

    def __init__(self, points: list[Point] | tuple[Point]):
        """Initialization method.

        Args:
            points: List or tuple of points.

        Raises:
            TypeError: If points is not a list or tuple
            ValueError: If points has less than two elements.
            TypeError: If elements of points are not of type Point.
        """
        if not isinstance(points, (tuple, list)):
            raise TypeError(f"{points!r} is not a tuple or list")
        self.points = tuple(points)

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
    def start(self) -> NDArray3[np.float64]:
        x, y, z = self.path(0)
        return Point(x, y, z)

    @property
    def end(self) -> NDArray3[np.float64]:
        x, y, z = self.path(1)
        return Point(x, y, z)

    @property
    def length(self) -> float:
        distance = 0.0
        xyz0 = self.path(0)
        for u in np.linspace(start=0, stop=1, num=NUM_POINTS, endpoint=True):
            xyz1 = self.path(u)
            distance += np.sqrt(np.sum((xyz1 - xyz0) ** 2))
            xyz0 = xyz1
        return distance

    def path(self, u: int | float, flip: bool = False) -> NDArray3[np.float64]:
        u = validate_curve_path_parameters(u, flip)

        def bezier(points, t):
            """Recursive bezier curve definition.

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
        for point in self.points:
            point.move(dx, dy, dz)
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
        for point in self.points:
            point.rotate(angle, a, b, c, x0, y0, z0)
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
        for point in self.points:
            point.mirror(a, b, c, x0, y0, z0)
        return self
