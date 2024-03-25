"""Module includes the Arc3 class
"""

import math
import numpy as np

from pygdf.auxiliary.point import Point
from pygdf.curves.curve import Curve, validate_path_parameter, validate_curve_path_input
from pygdf.utils.typing import NDArray3
from pygdf.utils.descriptors import AsInstanceOf, AsNDArray

TOLERANCE = 0.000001


class Arc3P(Curve):
    """Circular arc generated from 3 points in space.

    Implementation based on: https://en.wikipedia.org/wiki/Rodrigues%27_rotation_formula
    """

    centre = AsNDArray(shape=(3,))
    inverse_sector = AsInstanceOf(bool)

    def __init__(
        self,
        centre: Point,
        start: Point,
        end: Point,
        inverse_sector: bool = False,
    ):
        validate_input_types(centre, start, end, inverse_sector)
        validate_radii_and_cross_product(centre, start, end)
        self.centre = centre.xyz
        self.start = start.xyz
        self.end = end.xyz
        self.inverse_sector = inverse_sector

    @property
    def point_start(self) -> Point:
        xyz = self.start
        return Point(xyz[0], xyz[1], xyz[2])

    @property
    def point_end(self) -> Point:
        xyz = self.end
        return Point(xyz[0], xyz[1], xyz[2])

    def __eq__(self, other):
        return (
            np.all(self.centre == other.centre)
            and np.all(self.start == other.start)
            and np.all(self.end == other.end)
        )

    def __repr__(self):
        cls = type(self).__name__
        c, s, e, i = self.centre, self.start, self.end, self.inverse_sector
        c = Point(c[0], c[1], c[2])
        s = Point(s[0], s[1], s[2])
        e = Point(e[0], e[1], e[2])
        return f"{cls}(centre={c}, start={s}, end={e}, inverse_sector={i})"

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

    def path(self, u: int | float) -> NDArray3[np.float64]:
        u = validate_path_parameter(u)
        v, k, a = (self.start - self.centre), self.plane_unit_normal, self.angle
        xyz0 = self.centre
        part1 = v * math.cos(a * u)
        part2 = np.cross(k, v) * math.sin(a * u)
        part3 = k * np.dot(k, v) * (1 - math.cos(a * u))
        return xyz0 + part1 + part2 + part3

    def get_path_fn(self, flip_direction: bool = False):
        def fn(
            u: int | float, flip_direction: bool = flip_direction
        ) -> NDArray3[np.float64]:
            """Arc3P path function mapping input float from 0 to 1 to a physical xyz point"""
            u = validate_curve_path_input(u=u, flip_direction=flip_direction)
            v, k, a = (self.start - self.centre), self.plane_unit_normal, self.angle
            xyz0 = self.centre
            dxyz1 = v * math.cos(a * u)
            dxyz2 = np.cross(k, v) * math.sin(a * u)
            dxyz3 = k * np.dot(k, v) * (1 - math.cos(a * u))
            return xyz0 + dxyz1 + dxyz2 + dxyz3

        return fn


def validate_input_types(
    centre: Point, start: Point, end: Point, inverse_sector: bool
) -> None:
    if not isinstance(centre, Point):
        raise TypeError("centre is not of type 'Point'")
    if not isinstance(start, Point):
        raise TypeError("start is not of type 'Point'")
    if not isinstance(end, Point):
        raise TypeError("end is not of type 'Point'")
    if not isinstance(inverse_sector, bool):
        raise TypeError("inverse_sector is not of type 'bool'")


def validate_radii_and_cross_product(centre: Point, start: Point, end: Point) -> None:
    radius_start = np.sqrt(np.sum((start.xyz - centre.xyz)) ** 2)
    radius_end = np.sqrt(np.sum((end.xyz - centre.xyz) ** 2))
    if np.abs(radius_end - radius_start) / radius_start > TOLERANCE:
        raise ValueError("Resulting radii at start and end are different")
    cross_product = np.cross((start.xyz - centre.xyz), (end.xyz - centre.xyz))
    if np.all(cross_product == 0):
        raise ValueError("Resulting cross product is zero")
