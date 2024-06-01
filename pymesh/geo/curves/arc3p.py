"""Module containing the Arc3P class"""

import math
from typing import Self

import numpy as np

from pymesh.other.descriptors import AsInstanceOf
from pymesh.geo.curves.curve import Curve
from pymesh.geo.point import Point
from pymesh.other.typing import NDArray3
from pymesh.other.utils import validate_curve_path_parameters


ATOL = 0.000001


class Arc3P(Curve):
    """Creates an arc curve object, generated from three points in space.

    Implementation based on [WikiPedia](https://en.wikipedia.org/wiki/Rodrigues%27_rotation_formula).
    For more information, see Curve documentation.

    Args:
        centre (Point): Arc center point
        inverse_sector (bool): Specifies if to use the outer
            (True) or inner (False) sector of the swept circle.
            Defaults to False.
    """

    centre = AsInstanceOf(Point)
    inverse_sector = AsInstanceOf(bool)

    def __init__(
        self,
        centre: Point,
        start: Point,
        end: Point,
        inverse_sector: bool = False,
    ):
        """Initialization method.

        Args:
            centre: Arc center point
            start: Arc start point
            end: Arc end point
            inverse_sector: Specifies if to use the outer (True)
                or inner (False) sector of the swept circle.
                Defaults to False.

        Raises:
            ValueError: If the start and end points are located
                at different radii from the centre point.
            ValueError: If cross product of the centre-to-start
                and centre-to-end vectors is zero.
        """
        self.centre = centre
        self.start = start
        self.end = end
        self.inverse_sector = inverse_sector
        validate_radii_and_cross_product(centre, start, end)

    def __eq__(self, other):
        return (
            self.centre == other.centre
            and self.start == other.start
            and self.end == other.end
        )

    def __ne__(self, other):
        return not self.__eq__(other)

    def __repr__(self):
        cls = type(self).__name__
        c, s, e, i = self.centre, self.start, self.end, self.inverse_sector
        return f"{cls}(centre={c}, start={s}, end={e}, inverse_sector={i})"

    def copy(self) -> Self:
        return Arc3P(
            self.centre.copy(), self.start.copy(), self.end.copy(), self.inverse_sector
        )

    def move(
        self, dx: int | float = 0.0, dy: int | float = 0.0, dz: int | float = 0.0
    ) -> Self:
        self.centre.move(dx, dy, dz)
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
        self.centre.rotate(angle, a, b, c, x0, y0, z0)
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
        self.centre.mirror(a, b, c, x0, y0, z0)
        self.start.mirror(a, b, c, x0, y0, z0)
        self.end.mirror(a, b, c, x0, y0, z0)
        return self

    @property
    def radius(self) -> float:
        return np.sqrt(np.sum((self.start - self.centre) ** 2))

    @property
    def cross_product(self) -> NDArray3[np.float64]:
        sign = -1 if self.inverse_sector else 1
        return sign * np.cross((self.start - self.centre), (self.end - self.centre))

    @property
    def plane_unit_normal(self) -> NDArray3[np.float64]:
        return self.cross_product / np.sqrt(np.sum(self.cross_product**2))

    @property
    def angle(self) -> float:
        angle = np.arccos(
            np.dot((self.start - self.centre), (self.end - self.centre))
            / (self.radius**2)
        )
        angle = 2 * math.pi - angle if self.inverse_sector else angle
        return angle

    @property
    def length(self) -> float:
        return self.radius * self.angle

    def path(self, u: int | float, flip: bool = False) -> NDArray3[np.float64]:
        u = validate_curve_path_parameters(u, flip)
        v, k, a = (self.start - self.centre), self.plane_unit_normal, self.angle
        xyz0 = self.centre.xyz
        part1 = v * math.cos(a * u)
        part2 = np.cross(k, v) * math.sin(a * u)
        part3 = k * np.dot(k, v) * (1 - math.cos(a * u))
        return xyz0 + part1 + part2 + part3


def validate_radii_and_cross_product(centre: Point, start: Point, end: Point) -> None:
    radius_start = np.sqrt(np.sum((start - centre) ** 2))
    radius_end = np.sqrt(np.sum((end - centre) ** 2))
    if np.abs(radius_end - radius_start) > ATOL:
        raise ValueError("Resulting radii at start and end are different")
    cross_product = np.cross((start - centre), (end - centre))
    if np.all(cross_product == 0):
        raise ValueError("Resulting cross product is zero")
