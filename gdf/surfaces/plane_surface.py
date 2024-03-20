"""Module including the plane surface class
"""

import numpy as np
from numpy import ndarray

from gdf.curves import Line
from gdf.constants import MeshConstants
from gdf.points import Point
from gdf.mesh.descriptors import BoundaryDistribution, MeshNumber
from gdf.surfaces import Surface

# ! Remove .line_01 and .line_02 from the class

class PlaneSurface(Surface):
    """Creates a plane surface based on three points in space
    and creates mesh points for generating panels.
    """

    dist_01 = BoundaryDistribution()
    dist_02 = BoundaryDistribution()
    num_points_01 = MeshNumber()
    num_points_02 = MeshNumber()

    def __init__(self, point0:Point, point1:Point, point2:Point):
        self._all_surfaces.append(self)
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
        line1 = self.line_01.get_path_fn()
        line2 = self.line_02.get_path_fn()
        np1 = self.num_points_01
        np2 = self.num_points_02
        dist1 = self.dist_01.get_fn()
        dist2 = self.dist_02.get_fn()
        mp = np.zeros((3, np1, np2))
        for i, u in enumerate(np.linspace(0, 1, num=np1, endpoint=True)):
            for j, w in enumerate(np.linspace(0, 1, num=np2, endpoint=True)):
                mp[:, i, j] = line1(dist1(u)) + line2(dist2(w))
        return mp
