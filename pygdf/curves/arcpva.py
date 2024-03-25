"""Module includes the ArcVA class
"""

import math
import numpy as np

from pygdf.auxiliary.point import Point
from pygdf.auxiliary.vector3d import Vector3D
from pygdf.curves.curve import Curve, validate_path_parameter, validate_curve_path_input
from pygdf.custom_types import NDArray3
from pygdf.descriptors import AsInstanceOf, AsNumber

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

    @property
    def point_start(self) -> Point:
        xyz = self.start
        return Point(xyz[0], xyz[1], xyz[2])

    @property
    def point_end(self) -> Point:
        xyz = self.path(1)
        return Point(xyz[0], xyz[1], xyz[2])

    def __eq__(self, other):
        is_equal = True
        for u in np.linspace(0, 1, num=100, endpoint=True):
            if np.all(self.path(u) != other.path(u)):
                is_equal = False
                break
        return is_equal

    def __repr__(self):
        cls = type(self).__name__
        point = Point(self.start[0], self.start[1], self.start[2])
        txt = f"{cls}(start={point}, " f"axis={self.axis}, angle={self.angle})"
        return txt

    @property
    def radius(self) -> float:
        a = self.start - self.axis.start
        b = self.axis.end - self.axis.start
        r = a - np.dot(a, b) / np.dot(b, b) * b
        return np.sqrt(np.sum(r**2))

    @property
    def length(self) -> float:
        return self.radius * self.angle

    def path(self, u: int | float) -> NDArray3[np.float64]:
        u = validate_path_parameter(u)
        pvec = self.start - self.axis.start
        avec = self.axis.end - self.axis.start
        angle = self.angle
        xyz0 = self.axis.start
        part1 = pvec * math.cos(angle * u)
        part2 = np.cross(avec, pvec) * math.sin(angle * u)
        part3 = avec * np.dot(avec, pvec) * (1 - math.cos(angle * u))
        return xyz0 + part1 + part2 + part3

    def get_path_fn(self, flip_direction: bool = False):
        def fn(
            u: int | float, flip_direction: bool = flip_direction
        ) -> NDArray3[np.float64]:
            """ArcPVA path function mapping input float from 0 to 1 to a physical xyz point"""
            u = validate_curve_path_input(u=u, flip_direction=flip_direction)
            vp = self.start - self.axis.start
            va = self.axis.end - self.axis.start
            a = self.angle
            xyz0 = self.axis.start
            dxyz1 = vp * math.cos(a * u)
            dxyz2 = np.cross(va, vp) * math.sin(a * u)
            dxyz3 = va * np.dot(va, vp) * (1 - math.cos(a * u))
            return xyz0 + dxyz1 + dxyz2 + dxyz3

        return fn
