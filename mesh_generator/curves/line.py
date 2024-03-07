"""Module including linee class
"""

import numpy as np

from .curve import Curve
from ..point import Point
from ..mesh import DistributionMethod

class Line(Curve):
    """Line generated from two points in space.
    point_start is the starting point and point_end is the ending point.
    """

    def __init__(self, point_start: Point, point_end: Point):
        assert(isinstance(point_start, Point) and isinstance(point_end, Point)), \
            "Line arguments must be instances of the Point class."
        assert(point_start != point_end), "Line points must be unique."
        self.point_start = point_start
        self.point_end = point_end

    def __eq__(self, other):
        return self.point_start == other.point_start and self.point_end == other.point_end

    def __repr__(self):
        return f"{self.__class__.__name__}({self.point_start}, {self.point_end})"

    def get_path_fn(self):
        def path_fn(num_points:int, dist_method:DistributionMethod):
            dist_fn = dist_method.get_fn()
            path_xyz = np.zeros((num_points, 3))
            for i, u in enumerate(np.linspace(0, 1, num_points, endpoint=True)):
                path_xyz[i, :] = self.point_start.xyz \
                    + (self.point_end.xyz - self.point_start.xyz) * dist_fn(u)
            return path_xyz
        return path_fn
