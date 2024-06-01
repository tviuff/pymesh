from typing import Self

import numpy as np

from pymesh.other.descriptors import AsInstanceOf
from pymesh.geo.point import Point
from pymesh.geo.surfaces.surface import Surface
from pymesh.other.typing import NDArray3
from pymesh.other.utils import validate_surface_path_parameters


class BilinearSurface(Surface):
    """Creates a bilinear surface from the points p00, p10, p11 and p01.

    These four points represent the surface corners going counter-clockwise.
    The first number represents the value of u, while the second number
    represents the value of w.

    Attributes:
        p00 (Point): Bottom-left point (u=0, w=0).
        p10 (Point): Bottom-right point (u=1, w=0).
        p01 (Point): Top-left point (u=0, w=1).
        p11 (Point): Top-right point (u=1, w=1).
    """

    p00 = AsInstanceOf(Point)
    p10 = AsInstanceOf(Point)
    p01 = AsInstanceOf(Point)
    p11 = AsInstanceOf(Point)

    def __init__(self, p00: Point, p10: Point, p11: Point, p01: Point):
        """Initialization method.

        Args:
            p00: Bottom-left point
            p10: Bottom-right point
            p01: Top-left point
            p11: Top-right point

        Raises:
            TypeError: If p00, p10, p01 or p11 are not of type Point.
        """
        self._all_surfaces.append(self)
        self.p00 = p00
        self.p10 = p10
        self.p11 = p11
        self.p01 = p01

    def __eq__(self, other):
        return (
            self.p00 == other.p00
            and self.p10 == other.p10
            and self.p11 == other.p11
            and self.p01 == other.p01
        )

    def __repr__(self):
        return (
            f"{type(self).__name__}(p00={self.p00!r},"
            f"p10={self.p10!r}, p11={self.p11!r}, p01={self.p01!r})"
        )

    def path(
        self, u: int | float, w: int | float, uflip: bool = False, wflip: bool = False
    ) -> NDArray3[np.float64]:
        u, w = validate_surface_path_parameters(u, w, uflip, wflip)
        return (
            (1 - u) * w * self.p00.xyz
            + u * w * self.p10.xyz
            + (1 - u) * (1 - w) * self.p01.xyz
            + u * (1 - w) * self.p11.xyz
        )

    def get_max_lengths(self) -> tuple[float]:
        length_u_bottom = np.sqrt(np.sum((self.p00 - self.p10) ** 2))
        length_u_top = np.sqrt(np.sum((self.p01 - self.p11) ** 2))
        length_w_left = np.sqrt(np.sum((self.p00 - self.p01) ** 2))
        length_w_right = np.sqrt(np.sum((self.p10 - self.p11) ** 2))
        length_u = float(np.max((length_u_bottom, length_u_top)))
        length_w = float(np.max((length_w_left, length_w_right)))
        return length_u, length_w

    def copy(self) -> Self:
        copy = BilinearSurface(
            self.p00.copy(),
            self.p10.copy(),
            self.p11.copy(),
            self.p01.copy(),
        )
        copy._is_normal_flipped = self._is_normal_flipped
        return copy

    def move(
        self, dx: int | float = 0.0, dy: int | float = 0.0, dz: int | float = 0.0
    ) -> Self:
        self.p00.move(dx, dy, dz)
        self.p10.move(dx, dy, dz)
        self.p11.move(dx, dy, dz)
        self.p01.move(dx, dy, dz)
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
        self.p00.rotate(angle, a, b, c, x0, y0, z0)
        self.p10.rotate(angle, a, b, c, x0, y0, z0)
        self.p11.rotate(angle, a, b, c, x0, y0, z0)
        self.p01.rotate(angle, a, b, c, x0, y0, z0)
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
        self.p00.mirror(a, b, c, x0, y0, z0)
        self.p10.mirror(a, b, c, x0, y0, z0)
        self.p11.mirror(a, b, c, x0, y0, z0)
        self.p01.mirror(a, b, c, x0, y0, z0)
        return self
