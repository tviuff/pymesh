from typing import Self

import numpy as np

from pymesh.other.descriptors import AsInstanceOf
from pymesh.geo.point import Point
from pymesh.geo.surfaces.surface import Surface
from pymesh.other.typing import NDArray3
from pymesh.other.utils import validate_surface_path_parameters


class PlaneSurface(Surface):
    """Creates a plane surface based on three points in space.

    The plane is drawn from the vectors |point1 - point0| and
    |point2 - point0|, where point0 is a shared point between
    the two vectors.

    Attributes:
        point0 (Point): Shared point between two plane defining vectors.
        point1 (Point): Point defining the |point1-point0| vector.
        point2 (Point): Point defining the |point2-point0| vector.
    """

    point0 = AsInstanceOf(Point)
    point1 = AsInstanceOf(Point)
    point2 = AsInstanceOf(Point)

    def __init__(self, point0: Point, point1: Point, point2: Point):
        """Initialiation method.

        Args:
            point0: Shared point between two plane defining vectors.
            point1: Point defining the |point1-point0| vector.
            point2: Point defining the |point2-point0| vector.

        Raises:
            TypeError: If point0, point1 or point2 are not of type Point.
        """
        self._all_surfaces.append(self)
        self.point0 = point0
        self.point1 = point1
        self.point2 = point2

    def __eq__(self, other):
        return (
            self.point0 == other.point0
            and self.point1 == other.point1
            and self.point2 == other.point2
        )

    def __repr__(self):
        return (
            f"{type(self).__name__}(point0={self.point0!r},"
            f"point1={self.point1!r}, point2={self.point2!r})"
        )

    def path(
        self, u: int | float, w: int | float, uflip: bool = False, wflip: bool = False
    ) -> NDArray3[np.float64]:
        # ! find a way to add np.ndarray to Point using __add__
        u, w = validate_surface_path_parameters(u, w, uflip, wflip)
        xyz0 = self.point0.xyz
        u_point = (self.point1 - self.point0) * u
        w_point = (self.point2 - self.point0) * w
        return xyz0 + u_point + w_point

    def get_max_lengths(self) -> tuple[float]:
        length_u = float(np.sqrt(np.sum((self.point1 - self.point0) ** 2)))
        length_w = float(np.sqrt(np.sum((self.point2 - self.point0) ** 2)))
        return length_u, length_w

    def copy(self) -> Self:
        copy = PlaneSurface(self.point0.copy(), self.point1.copy(), self.point2.copy())
        copy._is_normal_flipped = self._is_normal_flipped
        return copy

    def move(
        self, dx: int | float = 0.0, dy: int | float = 0.0, dz: int | float = 0.0
    ) -> Self:
        self.point0.move(dx, dy, dz)
        self.point1.move(dx, dy, dz)
        self.point2.move(dx, dy, dz)
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
        self.point0.rotate(angle, a, b, c, x0, y0, z0)
        self.point1.rotate(angle, a, b, c, x0, y0, z0)
        self.point2.rotate(angle, a, b, c, x0, y0, z0)
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
        self.point0.mirror(a, b, c, x0, y0, z0)
        self.point1.mirror(a, b, c, x0, y0, z0)
        self.point2.mirror(a, b, c, x0, y0, z0)
        return self
