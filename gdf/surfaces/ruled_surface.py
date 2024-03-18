"""Module including the ruled surface class
"""

import numpy as np
from numpy import ndarray

from gdf.constants import MeshConstants
from gdf.curves import Curve
from gdf.mesh.descriptors import BoundaryDistribution, MeshNumber
from gdf.surfaces import Surface

# ! Not yet tested for dist_method_w

class RuledSurface(Surface):
    """Creates a ruled surface based on two curves
    and creates mesh points for generating panels.
    """

    dist1 = BoundaryDistribution()
    dist2 = BoundaryDistribution()
    num_points_u = MeshNumber()
    num_points_w = MeshNumber()

    def __init__(self, curve1:Curve, curve2:Curve):
        self.curve1 = curve1
        self.curve2 = curve2
        self.dist1 = MeshConstants.DEFAULT_DIST_METHOD.value
        self.dist2 = MeshConstants.DEFAULT_DIST_METHOD.value
        self.num_points_u = MeshConstants.DEFAULT_NUM_POINT.value
        self.num_points_w = MeshConstants.DEFAULT_NUM_POINT.value

    @property
    def curve1(self) -> Curve:
        return self._curve1

    @curve1.setter
    def curve1(self, value) -> None:
        if not isinstance(value, Curve):
            raise TypeError("curve1 must be of type 'Curve'")
        self._curve1 = value

    @property
    def curve2(self) -> Curve:
        return self._curve2

    @curve2.setter
    def curve2(self, value) -> None:
        if not isinstance(value, Curve):
            raise TypeError("curve2 must be of type 'Curve'")
        self._curve2 = value

    @property
    def mesh_points(self) -> ndarray:
        curve1_xyz = self.curve1.get_path_xyz(
            num_points = self.num_points_u,
            dist_method = self.dist1
        )
        curve2_xyz = self.curve2.get_path_xyz(
            num_points = self.num_points_u,
            dist_method = self.dist2
        )
        mp = np.zeros((3, self.num_points_u, self.num_points_w))
        for u in range(0, self.num_points_u):
            for w in range(0, self.num_points_w):
                mp[:, u, w] = 0 \
                    + (1-w) * curve1_xyz[u, :] \
                    + w * curve2_xyz[u, :]
        return mp
