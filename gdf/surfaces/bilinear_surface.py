"""Module including the bilinear surface class
"""

import numpy as np
from numpy import ndarray

from gdf.constants import MeshConstants
from gdf.points import Point
from gdf.mesh import BoundaryDistribution, MeshNumber
from gdf.surfaces import Surface


class SurfaceCornerPoint:
    """Surface corner point descriptor class"""

    def __set_name__(self, owner, name):
        self._name = name

    def __get__(self, instance, owner) -> Point:
        return instance.__dict__[self._name]

    def __set__(self, instance, value):
        if not isinstance(value, Point):
            raise TypeError(f"{self._name} must be of type 'Point'")
        instance.__dict__[self._name] = value


class BilinearSurface(Surface):
    """Creates a bilinear surface based on four points in space
    and creates mesh points for generating panels.
    """

    point00 = SurfaceCornerPoint()
    point10 = SurfaceCornerPoint()
    point01 = SurfaceCornerPoint()
    point11 = SurfaceCornerPoint()
    dist_01 = BoundaryDistribution()
    dist_02 = BoundaryDistribution()
    num_points_01 = MeshNumber()
    num_points_02 = MeshNumber()

    def __init__(self, point00:Point, point10:Point, point01:Point, point11:Point):
        self.point00 = point00
        self.point10 = point10
        self.point01 = point01
        self.point11 = point11
        self.dist_01 = MeshConstants.DEFAULT_DIST_METHOD.value
        self.dist_02 = MeshConstants.DEFAULT_DIST_METHOD.value
        self.num_points_01 = MeshConstants.DEFAULT_NUM_POINT.value
        self.num_points_02 = MeshConstants.DEFAULT_NUM_POINT.value

    @property
    def mesh_points(self) -> ndarray:
        mp = np.zeros((3, self.num_points_01, self.num_points_02))
        for i, u in enumerate(range(0, self.num_points_01)):
            for j, w in enumerate(range(0, self.num_points_02)):
                mp[:, i, j] = 0 \
                    + (1-u) * (1-w) * self.point00.xyz \
                    + u * (1-w) * self.point10.xyz \
                    + (1-u) * w * self.point01.xyz \
                    + u * w * self.point11.xyz
        return mp
