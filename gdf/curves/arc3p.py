"""Module includes the Arc3 class
"""

import math
import numpy as np
from numpy import ndarray

from gdf.points import Point
from gdf.mesh.distribution_methods import DistMethod
from gdf.constants import MeshConstants
from .curve import Curve

class Arc3P(Curve):
    """Circular arc generated from 3 points in space.

    Implementation based on: https://en.wikipedia.org/wiki/Rodrigues%27_rotation_formula
    """

    def __init__(self,
            point_centre:Point, point_start:Point, point_end:Point,
            flipped_dir:bool=False
        ):
        self.point_centre = point_centre
        self.point_start = point_start
        self.point_end = point_end
        self.flipped_dir = flipped_dir
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
        """Returns the distance |point_start - point_centre|"""
        return np.sqrt(np.sum(self.vector_start**2))

    @property
    def flipped_dir(self) -> bool:
        return self._flipped_dir

    @flipped_dir.setter
    def flipped_dir(self, value:bool) -> None:
        if not isinstance(value, bool):
            raise TypeError("flip_direction must be of type 'bool'")
        self._flipped_dir = value

    @property
    def cross_product(self) -> ndarray:
        vector_start = self.point_start.xyz - self.point_centre.xyz
        vector_end = self.point_end.xyz - self.point_centre.xyz
        sign = -1 if self.flipped_dir else 1
        return sign * np.cross(vector_start, vector_end)

    @property
    def plane_unit_normal(self) -> ndarray:
        return self.cross_product / np.sqrt(np.sum(self.cross_product**2))

    @property
    def angle(self) -> float:
        angle = np.arccos(np.dot(self.vector_start, self.vector_end) / ( self.radius**2 ))
        angle = 2*math.pi - angle if self.flipped_dir else angle
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

    def get_path_xyz(self,
            num_points:int = None,
            dist_method:DistMethod = None,
            flip_dir:bool = False
        ) -> ndarray:
        if num_points is None:
            num_points = MeshConstants.DEFAULT_NUM_POINT.value
        if dist_method is None:
            dist_method = MeshConstants.DEFAULT_DIST_METHOD.value
        path_xyz = np.zeros((num_points, 3))
        dist_fn = dist_method.get_fn(flip_dir)
        v, k, a = self.vector_start, self.plane_unit_normal, self.angle
        for i, u in enumerate(np.linspace(0, 1, num_points, endpoint=True)):
            path_xyz[i,:] = self.point_centre.xyz \
                    + v * math.cos(a * dist_fn(u)) \
                    + np.cross(k, v) * math.sin(a * dist_fn(u)) \
                    + k * np.dot(k, v) * (1 - math.cos(a * dist_fn(u)))
        return path_xyz
