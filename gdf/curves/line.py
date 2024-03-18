"""Module including line class
"""

import numpy as np
from numpy import ndarray

from gdf.points import Point
from gdf.mesh.distribution_methods import DistMethod
from gdf.constants import MeshConstants
from .curve import Curve

class Line(Curve):
    """Line generated from two points in space"""

    def __init__(self, point_start: Point, point_end: Point):
        self.point_start = point_start
        self.point_end = point_end
        self._validate_input()

    def _validate_input(self) -> None:
        if self.point_start == self.point_end:
            raise ValueError(f"{type(self).__name__} input points must be unique.")

    def __eq__(self, other):
        return self.point_start == other.point_start and self.point_end == other.point_end

    def __repr__(self):
        return f"{type(self).__name__}({self.point_start}, {self.point_end})"

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
    def length(self) -> float:
        return np.sqrt(np.sum((self.point_end.xyz-self.point_start.xyz)**2))

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
        for i, u in enumerate(np.linspace(0, 1, num_points, endpoint=True)):
            path_xyz[i, :] = self.point_start.xyz \
                + (self.point_end.xyz - self.point_start.xyz) * dist_fn(u)
        return path_xyz
