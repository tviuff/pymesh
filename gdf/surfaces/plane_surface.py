"""Module including the plane surface class
"""

import numpy as np
from numpy import ndarray

from gdf.constants import MeshConstants
from gdf.points import Point
from gdf.mesh.descriptors import BoundaryDistribution, MeshNumber
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

class PlaneSurface(Surface):
    """Creates a plane surface based on three points in space
    and creates mesh points for generating panels.
    """

    point0 = SurfaceCornerPoint()
    point1 = SurfaceCornerPoint()
    point2 = SurfaceCornerPoint()
    dist01 = BoundaryDistribution()
    dist02 = BoundaryDistribution()
    num_points_01 = MeshNumber()
    num_points_02 = MeshNumber()

    def __init__(self, point0:Point, point1:Point, point2:Point):
        self._all_surfaces.append(self)
        self.point0 = point0
        self.point1 = point1
        self.point2 = point2
        self.dist01 = MeshConstants.DEFAULT_DIST_METHOD.value()
        self.dist02 = MeshConstants.DEFAULT_DIST_METHOD.value()
        self.num_points_01 = MeshConstants.DEFAULT_NUM_POINT.value
        self.num_points_02 = MeshConstants.DEFAULT_NUM_POINT.value

    @property
    def mesh_points(self) -> ndarray:

        def line1(u):
            fn = self.dist01.get_fn()
            return self.point0.xyz + (self.point1.xyz - self.point0.xyz)*fn(u)

        def line2(u):
            fn = self.dist02.get_fn()
            return self.point0.xyz + (self.point2.xyz - self.point0.xyz)*fn(u)

        np1 = self.num_points_01
        np2 = self.num_points_02
        mp = np.zeros((3, np1, np2))
        for i, u in enumerate(np.linspace(0, 1, num=np1, endpoint=True)):
            for j, w in enumerate(np.linspace(0, 1, num=np2, endpoint=True)):
                mp[:, i, j] = line1(u) + line2(w)
        return mp
