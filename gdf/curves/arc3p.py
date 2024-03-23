"""Module includes the Arc3 class
"""

import math
import numpy as np
from numpy import ndarray

from gdf.auxiliary.point import Point
from gdf.curves.curve import Curve, validate_curve_path_fn_input

class Arc3P(Curve):
    """Circular arc generated from 3 points in space.

    Implementation based on: https://en.wikipedia.org/wiki/Rodrigues%27_rotation_formula
    """

    def __init__(self,
            point_centre:Point,
            point_start:Point,
            point_end:Point,
            invert_arc:bool=False
        ):
        self.point_centre = point_centre
        self.point_start = point_start
        self.point_end = point_end
        self.invert_arc = invert_arc
        self._tolerance = 0.0001
        self._validate_input()

    @property
    def point_centre(self) -> Point:
        return self._point_centre

    @point_centre.setter
    def point_centre(self, point:Point) -> None:
        if not isinstance(point, Point):
            raise TypeError("point_centre must be of type 'Point'")
        self._point_centre = point

    @property
    def point_start(self) -> Point:
        return self._point_start

    @point_start.setter
    def point_start(self, point:Point) -> None:
        if not isinstance(point, Point):
            raise TypeError("point_start must be of type 'Point'")
        self._point_start = point

    @property
    def point_end(self) -> Point:
        return self._point_end

    @point_end.setter
    def point_end(self, point:Point) -> None:
        if not isinstance(point, Point):
            raise TypeError("point_end must be of type 'Point'")
        self._point_end = point

    @property
    def vector_start(self) -> ndarray:
        return self.point_start.xyz - self.point_centre.xyz

    @property
    def vector_end(self) -> ndarray:
        return self.point_end.xyz - self.point_centre.xyz

    @property
    def radius(self) -> float:
        """Returns the length |vector_start|"""
        return np.sqrt(np.sum(self.vector_start**2))

    @property
    def invert_arc(self) -> bool:
        return self._invert_arc

    @invert_arc.setter
    def invert_arc(self, value:bool) -> None:
        if not isinstance(value, bool):
            raise TypeError("invert_arc must be of type 'bool'")
        self._invert_arc = value

    @property
    def cross_product(self) -> ndarray:
        vector_start = self.point_start.xyz - self.point_centre.xyz
        vector_end = self.point_end.xyz - self.point_centre.xyz
        sign = -1 if self.invert_arc else 1
        return sign * np.cross(vector_start, vector_end)

    @property
    def plane_unit_normal(self) -> ndarray:
        return self.cross_product / np.sqrt(np.sum(self.cross_product**2))

    @property
    def angle(self) -> float:
        angle = np.arccos(np.dot(self.vector_start, self.vector_end) / ( self.radius**2 ))
        angle = 2*math.pi - angle if self.invert_arc else angle
        return angle

    @property
    def length(self) -> float:
        return self.radius * self.angle

    def _validate_input(self) -> None:
        diff_radii = np.sqrt(np.sum(self.vector_end**2)) - np.sqrt(np.sum(self.vector_start**2))
        radius_start = np.sqrt(np.sum(self.vector_start**2))
        if (diff_radii / radius_start) > self._tolerance:
            raise ValueError(
                f"Input points resulted in " \
                f"(radius_end - radius_start)  > {self._tolerance} x radius_start"
                )
        if (self.cross_product == 0).all():
            raise ValueError("Input points resulted in parallel plane vectors")

    def __eq__(self, other):
        return self.point_centre == other.point_centre \
            and self.point_start == other.point_start \
                and self.point_end == other.point_end

    def __repr__(self):
        return f"{type(self).__name__}({self.point_centre}, {self.point_start}, {self.point_end})"

    def get_path_fn(self, flip_direction:bool=False):
        def fn(u:int|float, flip_direction:bool=flip_direction) -> ndarray:
            """Arc3P path function mapping input float from 0 to 1 to a physical xyz point"""
            u = validate_curve_path_fn_input(u=u, flip_direction=flip_direction)
            v, k, a = self.vector_start, self.plane_unit_normal, self.angle
            xyz0 = self.point_centre.xyz
            dxyz1 = v * math.cos(a * u)
            dxyz2 = np.cross(k, v) * math.sin(a * u)
            dxyz3 = k * np.dot(k, v) * (1 - math.cos(a * u))
            return xyz0 + dxyz1 + dxyz2 + dxyz3
        return fn
