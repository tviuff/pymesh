"""Module including line class
"""

import numpy as np
from numpy import ndarray

from gdfgen.point import Point
from gdfgen.mesh import DistMethod
from gdfgen.constants import MeshConstants
from .curve import Curve

class Line(Curve):
    """Line generated from two points in space"""

    def __init__(self, point_start: Point, point_end: Point):
        super().__init__(point_start, point_end)
        self._validate_input()

    def _validate_input(self) -> None:
        if self.point_start == self.point_end:
            raise ValueError(f"{type(self).__name__} input points must be unique.")

    def __eq__(self, other):
        return self.point_start == other.point_start and self.point_end == other.point_end

    def __repr__(self):
        return f"{type(self).__name__}({self.point_start}, {self.point_end})"

    def get_path_xyz(self,
            num_points:int = MeshConstants.DEFAULT_NUM_POINT.value,
            dist_method:DistMethod = MeshConstants.DEFAULT_DIST_METHOD.value,
            flip_dir:bool = False
        ) -> ndarray:
        path_xyz = np.zeros((num_points, 3))
        dist_fn = dist_method.get_fn(flip_dir)
        for i, u in enumerate(np.linspace(0, 1, num_points, endpoint=True)):
            path_xyz[i, :] = self.point_start.xyz \
                + (self.point_end.xyz - self.point_start.xyz) * dist_fn(u)
        return path_xyz
