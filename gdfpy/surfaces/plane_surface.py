"""Module including the plane surface class
"""

import numpy as np
from numpy import ndarray

from gdfpy import Line
from gdfpy.constants import MeshConstants
from gdfpy.points import Point
from gdfpy.mesh import BoundaryDistribution, MeshNumber
from gdfpy.surfaces import Surface

class PlaneSurface(Surface):
    """Creates a plane surface based on three points in space
    and creates mesh points for generating panels.
    """

    dist_01 = BoundaryDistribution()
    dist_02 = BoundaryDistribution()
    num_points_01 = MeshNumber()
    num_points_02 = MeshNumber()

    def __init__(self, point0:Point, point1:Point, point2:Point):
        self.line_01 = Line(point_start=point0, point_end=point1)
        self.line_02 = Line(point_start=point0, point_end=point2)
        self.dist_01 = MeshConstants.DEFAULT_DIST_METHOD.value
        self.dist_02 = MeshConstants.DEFAULT_DIST_METHOD.value
        self.num_points_01 = MeshConstants.DEFAULT_NUM_POINT.value
        self.num_points_02 = MeshConstants.DEFAULT_NUM_POINT.value

    @property
    def line_01(self)-> Line:
        return self._line_01

    @line_01.setter
    def line_01(self, value:Line) -> None:
        if not isinstance(value, Line):
            raise TypeError("line_01 must be of type 'Line'")
        self._line_01 = value

    @property
    def line_02(self)-> Line:
        return self._line_02

    @line_02.setter
    def line_02(self, value:Line) -> None:
        if not isinstance(value, Line):
            raise TypeError("line_02 must be of type 'Line'")
        self._line_02 = value

    @property
    def mesh_points(self) -> ndarray:
        xyz_line_01 = self.line_01.get_path_xyz(
            num_points = self.num_points_01,
            dist_method = self.dist_02
            )
        xyz_line_02 = self.line_02.get_path_xyz(
            num_points = self.num_points_02,
            dist_method = self.dist_01
            )
        mp = np.zeros((3, self.num_points_01, self.num_points_02))
        for i in range(0, self.num_points_01):
            for j in range(0, self.num_points_02):
                for k in range(0, 3):
                    mp[k, i, j] = xyz_line_01[i, k] + xyz_line_02[j, k]
        return mp
