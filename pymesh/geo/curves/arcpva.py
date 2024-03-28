"""Module includes the ArcVA class
"""

import math
import numpy as np
from typing import Self

from pymesh.descriptors import AsInstanceOf, AsNumber
from pymesh.geo.point import Point
from pymesh.geo.curves.curve import Curve
from pymesh.geo.vector3d import Vector3D
from pymesh.typing import NDArray3
from pymesh.utils import validate_move_parameters, validate_curve_path_parameters

# ! Keep constructor as is for now


class ArcPVA(Curve):
    """Circular arc generated from a point, an axis of rotation and an angle (rad).
    For more iformation, see https://en.wikipedia.org/wiki/Rodrigues%27_rotation_formula.
    """

    axis = AsInstanceOf(Vector3D)
    angle = AsNumber(return_type=float)

    def __init__(self, point: Point, axis: Vector3D, angle: int | float):
        self.start = point.xyz
        self.axis = axis
        self.angle = angle

    @property
    def end(self) -> NDArray3[np.float64]:
        return self.path(1)

    # def __eq__(self, other):
    #     eq_start = np.all(self.start == other.start)
    #     eq_end = np.all(self.end == other.end)
    #     eq_axis = np.all(self.axis.start == other.axis.start)
    #     eq_angle = self.angle == other.angle
    #     return eq_start and eq_end and eq_axis and eq_angle

    def __eq__(self, other):
        DECIMALS = 4
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
        point = Point(self.start[0], self.start[1], self.start[2])
        txt = f"{cls}(start={point}, " f"axis={self.axis}, angle={self.angle:.2f})"
        return txt

    def copy(self) -> Self:
        start = Point(self.start[0], self.start[1], self.start[2])
        return ArcPVA(start, self.axis.copy(), self.angle)  # ! how to copy float ??

    def move(
        self, dx: int | float = 0.0, dy: int | float = 0.0, dz: int | float = 0.0
    ) -> None:
        validate_move_parameters(dx, dy, dz)
        dxyz = np.array([dx, dy, dz])
        self.start += dxyz  # self.end is a derrived property and is not moved
        self.axis.move(dx, dy, dz)

    @property
    def radius(self) -> float:
        a = self.start - self.axis.start
        b = self.axis.end - self.axis.start
        r = a - np.dot(a, b) / np.dot(b, b) * b
        return np.sqrt(np.sum(r**2))

    @property
    def length(self) -> float:
        return self.radius * self.angle

    def path(self, u: int | float, flip: bool = False) -> NDArray3[np.float64]:
        u = validate_curve_path_parameters(u, flip)
        pvec = self.start - self.axis.start
        avec = self.axis.end - self.axis.start
        angle = self.angle
        xyz0 = self.axis.start
        part1 = pvec * math.cos(angle * u)
        part2 = np.cross(avec, pvec) * math.sin(angle * u)
        part3 = avec * np.dot(avec, pvec) * (1 - math.cos(angle * u))
        return xyz0 + part1 + part2 + part3
