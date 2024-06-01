"""Module containing the ArcPVA class"""

import math
from typing import Self
import numpy as np

from pymesh.descriptors import AsNumber
from pymesh.geo.point import Point
from pymesh.geo.curves.curve import Curve
from pymesh.typing import NDArray3
from pymesh.utils import (
    validate_curve_path_parameters,
    rotate_point_xyz,
    mirror_point_xyz,
)


class ArcPVA(Curve):
    """Creates a circular arc based on a point, a vector axis of rotation and an angle.

    Attributes:
        angle (int | float): Angle in radians.
            Positive direction defined as counter-clockwise, based on the right-hand rule.
        a (int | float): Axis vector x direction.
        b (int | float): Axis vector y direction.
        c (int | float): Axis vector z direction.
        x0 (int | float): Axis base x coordinate, default is zero.
        y0 (int | float): Axis base y coordinate, default is zero.
        z0 (int | float): Axis base z coordinate, default is zero.
    """

    angle = AsNumber(return_type=float)
    a = AsNumber(return_type=float)
    b = AsNumber(return_type=float)
    c = AsNumber(return_type=float)
    x0 = AsNumber(return_type=float)
    y0 = AsNumber(return_type=float)
    z0 = AsNumber(return_type=float)

    def __init__(
        self,
        start: Point,
        angle: int | float,
        a: int | float,
        b: int | float,
        c: int | float,
        x0: int | float = 0.0,
        y0: int | float = 0.0,
        z0: int | float = 0.0,
    ):
        """Initialization method.

        Args:
            start: Point being rotated around the vector.
            angle: Angle in radians.
                Positive direction defined as counter-clockwise, based on the right-hand rule.
            a: Axis vector x direction.
            b: Axis vector y direction.
            c: Axis vector z direction.
            x0: Axis base x coordinate, default is zero.
            y0: Axis base y coordinate, default is zero.
            z0: Axis base z coordinate, default is zero.
        """
        self.start = start
        self.angle = angle
        self.a = a
        self.b = b
        self.c = c
        self.x0 = x0
        self.y0 = y0
        self.z0 = z0

    @property
    def end(self) -> NDArray3[np.float64]:
        x, y, z = self.path(1)
        return Point(x, y, z)

    def __eq__(self, other):
        DECIMALS = 10
        is_equal = True
        for u in np.linspace(0, 1, num=100, endpoint=True):
            u_self = np.all(np.round(self.path(u), decimals=DECIMALS))
            u_other = np.all(np.round(other.path(u), decimals=DECIMALS))
            if u_self != u_other:
                is_equal = False
                break
        return is_equal

    def __ne__(self, other):
        return not self.__eq__(other)

    def __repr__(self):
        cls = type(self).__name__
        txt = (
            f"{cls}(start={self.start!r}, angle={self.angle:.2f}, "
            f"a={self.a:.2f}, b={self.b:.2f}, c={self.c:.2f}, "
            f"x0={self.x0:.2f}, y0={self.y0:.2f}, z0={self.z0:.2f})"
        )
        return txt

    @property
    def radius(self) -> float:
        """Returns the arc radius."""
        xyz0 = np.array([self.x0, self.y0, self.z0])
        a = self.start.xyz - xyz0
        b = np.array([self.a, self.b, self.c])
        r = a - np.dot(a, b) / np.dot(b, b) * b
        return np.sqrt(np.sum(r**2))

    @property
    def length(self) -> float:
        return self.radius * self.angle

    def path(self, u: int | float, flip: bool = False) -> NDArray3[np.float64]:
        u = validate_curve_path_parameters(u, flip)
        angle = self.angle
        xyz0 = np.array([self.x0, self.y0, self.z0])
        abc = np.array([self.a, self.b, self.c])
        pvec = self.start.xyz - xyz0
        part1 = pvec * math.cos(angle * u)
        part2 = np.cross(abc, pvec) * math.sin(angle * u)
        part3 = abc * np.dot(abc, pvec) * (1 - math.cos(angle * u))
        return xyz0 + part1 + part2 + part3

    def copy(self) -> Self:
        return ArcPVA(
            self.start.copy(),
            self.angle,
            self.a,
            self.b,
            self.c,
            self.x0,
            self.y0,
            self.z0,
        )

    def move(
        self, dx: int | float = 0.0, dy: int | float = 0.0, dz: int | float = 0.0
    ) -> Self:
        self.start.move(dx, dy, dz)  # also validates input
        self.x0 += float(dx)
        self.y0 += float(dy)
        self.z0 += float(dz)
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
        self.start.rotate(angle, a, b, c, x0, y0, z0)  # also validates input
        xyz0 = np.array([self.x0, self.y0, self.z0])
        xyz0_rotated = rotate_point_xyz(
            xyz0[0], xyz0[1], xyz0[2], angle, a, b, c, x0, y0, z0
        )
        xyz1_rotated = rotate_point_xyz(
            self.a + x0, self.b + y0, self.c + z0, angle, a, b, c, x0, y0, z0
        )
        self.x0, self.y0, self.z0 = xyz0_rotated
        self.a, self.b, self.c = xyz1_rotated - xyz0
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
        self.start.mirror(a, b, c, x0, y0, z0)  # validates input, should be first
        xyz0 = np.array([self.x0, self.y0, self.z0])
        xyz0_mirrored = mirror_point_xyz(xyz0[0], xyz0[1], xyz0[2], a, b, c, x0, y0, z0)
        xyz1_mirrored = mirror_point_xyz(
            self.a + x0, self.b + y0, self.c + z0, a, b, c, x0, y0, z0
        )
        self.x0, self.y0, self.z0 = xyz0_mirrored
        self.a, self.b, self.c = xyz1_mirrored - xyz0
        return self
