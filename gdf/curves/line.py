"""Module including line class
"""

import numpy as np
from numpy import ndarray

from gdf.points import Point
from .curve import Curve, validate_curve_path_fn_input

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

    def get_path_fn(self, flip_direction:bool=False):
        def fn(u:int|float, flip_direction:bool=flip_direction) -> ndarray:
            """Line path function mapping input float from 0 to 1 to a physical xyz point"""
            validate_curve_path_fn_input(u=u, flip_direction=flip_direction)
            if flip_direction:
                u = 1.0 - u
            xyz0 = self.point_start.xyz
            dxyz = self.point_end.xyz - self.point_start.xyz
            return xyz0 + dxyz * u
        return fn
