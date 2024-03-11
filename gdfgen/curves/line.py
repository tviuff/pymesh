"""Module including linee class
"""

import numpy as np

from gdfgen.point import Point
from gdfgen.mesh import DistMethod
from .curve import Curve

class Line(Curve):
    """Line generated from two points in space.
    point_start is the starting point and point_end is the ending point.
    """

    def __init__(self, point_start: Point, point_end: Point):
        super().__init__(point_start, point_end)
        if not (isinstance(point_start, Point) and isinstance(point_end, Point)):
            raise TypeError(f"{self.__class__.__name__} class only takes point input of type 'Point'.")
        if point_start == point_end:
            raise ValueError(f"{self.__class__.__name__} input points must be unique.")

    def __eq__(self, other):
        return self.point_start == other.point_start and self.point_end == other.point_end

    def __repr__(self):
        return f"{self.__class__.__name__}({self.point_start}, {self.point_end})"

    def get_path_fn(self, num_points:int, dist_method:DistMethod, flip_dir:bool=False):
        def path_fn():
            dist_fn = dist_method().get_fn(flip_dir)
            path_xyz = np.zeros((num_points, 3))
            for i, u in enumerate(np.linspace(0, 1, num_points, endpoint=True)):
                path_xyz[i, :] = self.point_start.xyz \
                    + (self.point_end.xyz - self.point_start.xyz) * dist_fn(u)
            return path_xyz
        return path_fn
