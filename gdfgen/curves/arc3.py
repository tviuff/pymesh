"""Module includes the Arc3 class
"""

import math
import numpy as np

from .curve import Curve
from gdfgen.point import Point
from gdfgen.mesh import DistributionMethod

class Arc3(Curve):
    """Circular arc generated from 3 points in space
    From https://en.wikipedia.org/wiki/Rodrigues%27_rotation_formula
    """

    point_centre:Point
    __tolerance = 0.0001

    def __init__(self, point_centre:Point, point_start:Point, point_end):
        super().__init__(point_start, point_end)
        self.point_centre, self.point_start, self.point_end = point_centre, point_start, point_end
        if not (isinstance(self.point_start, Point)
                and isinstance(self.point_end, Point)
                and isinstance(self.point_centre, Point)
                ):
            raise TypeError(f"{self.__class__.__name__} class only takes point inputs of type 'Point'.")
        if ((point_start == point_end)
                or (point_start == point_centre)
                or (point_end == point_centre)
                ):
            raise ValueError(f"{self.__class__.__name__} input points must be unique.")

    def __eq__(self, other):
        return self.point_centre == other.point_centre \
            and self.point_start == other.point_start \
                and self.point_end == other.point_end

    def __repr__(self):
        return f"{self.__class__.__name__}({self.point_centre}, {self.point_start}, {self.point_end})"

    def _get_path_fn_params(self) -> tuple:
        """Returns tuple of path function parameters: (vector_start, plane_unit_normal and angle)"""
        vector_start = self.point_start.xyz - self.point_centre.xyz
        radius_start = np.sqrt(np.sum(vector_start**2))
        unit_vector_start = vector_start/radius_start
        vector_end = self.point_end.xyz - self.point_centre.xyz
        radius_end = np.sqrt(np.sum(vector_end**2))
        unit_vector_end = vector_end/radius_end
        cross_prod = np.cross(vector_start, vector_end)
        plane_unit_normal = cross_prod / np.sqrt(np.sum(cross_prod**2))
        # ! Not sure if below is working..
        if ((cross_prod == 0).all() and (unit_vector_start == -unit_vector_end).all()):
            angle = math.pi
        elif ((cross_prod == 0).all() and (unit_vector_start == unit_vector_end).all()):
            angle = 0.
        else:
            angle = np.arccos(np.dot(vector_start, vector_end) / ( radius_start * radius_end ))
        return vector_start, plane_unit_normal, angle

    def get_path_fn(self):
        def path_fn(num_points:int, dist_method:DistributionMethod):
            dist_fn = dist_method.get_fn()
            path_xyz = np.zeros((num_points, 3))
            v, k, a = self._get_path_fn_params()
            for i, u in enumerate(np.linspace(0, 1, num_points, endpoint=True)):
                path_xyz[i,:] = self.point_centre.xyz \
                        + v * math.cos(a * dist_fn(u)) \
                        + np.cross(k, v) * math.sin(a * dist_fn(u)) \
                        + k * np.cross(k, v) * (1 - math.cos(a * dist_fn(u)))
            return path_xyz
        return path_fn
