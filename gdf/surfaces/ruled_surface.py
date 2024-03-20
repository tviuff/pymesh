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
    num_points_1 = MeshNumber()
    num_points_2 = MeshNumber()

    def __init__(self, curve1:Curve, curve2:Curve):
        self._all_surfaces.append(self)
        self.curve1 = curve1
        self.curve2 = curve2
        self.dist1 = MeshConstants.DEFAULT_DIST_METHOD.value
        self.dist2 = MeshConstants.DEFAULT_DIST_METHOD.value
        self.num_points_1 = MeshConstants.DEFAULT_NUM_POINT.value
        self.num_points_2 = MeshConstants.DEFAULT_NUM_POINT.value

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
        curve1 = self.curve1.get_path_fn()
        np1 = self.num_points_1
        dist1 = self.dist1.get_fn()
        curve2 = self.curve2.get_path_fn()
        np2 = self.num_points_2
        dist2 = self.dist2.get_fn()
        mp = np.zeros((3, np1, np2))
        for i, u in enumerate(np.linspace(0, 1, num=np1, endpoint=True)):
            for j, w in enumerate(np.linspace(0, 1, num=np2, endpoint=True)):
                mp[:, i, j] = (1-w)*curve1(dist1(u)) + w*curve2(dist2(u))
        return mp
