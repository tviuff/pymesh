"""Module including the swept surface class
"""

import numpy as np
from numpy import ndarray

from gdf.constants import MeshConstants
from gdf.curves import Curve
from gdf.mesh.descriptors import BoundaryDistribution, MeshNumber
from gdf.surfaces import Surface

# ! see SweptSurface.generate_mesh_points()

class SweptSurface(Surface):
    """Creates a surface based on a curve swept by another
    and creates mesh points for generating panels.
    """

    dist_curve = BoundaryDistribution()
    dist_sweeper_curve = BoundaryDistribution()
    num_points_curve = MeshNumber()
    num_points_sweeper_curve = MeshNumber()

    def __init__(self, curve:Curve, sweeper_curve:Curve):
        self._all_surfaces.append(self)
        self.curve = curve
        self.sweeper_curve = sweeper_curve
        self.dist_curve = MeshConstants.DEFAULT_DIST_METHOD.value()
        self.dist_sweeper_curve = MeshConstants.DEFAULT_DIST_METHOD.value()
        self.num_points_curve = MeshConstants.DEFAULT_NUM_POINT.value
        self.num_points_sweeper_curve = MeshConstants.DEFAULT_NUM_POINT.value

    @property
    def curve(self)-> Curve:
        return self._curve

    @curve.setter
    def curve(self, curve:Curve) -> None:
        if not isinstance(curve, Curve):
            raise TypeError("curve must be of type 'Curve'")
        self._curve = curve

    @property
    def sweeper_curve(self)-> Curve:
        return self._sweeper_curve

    @sweeper_curve.setter
    def sweeper_curve(self, value:Curve) -> None:
        if not isinstance(value, Curve):
            raise TypeError("sweeper_curve must be of type 'Curve'")
        self._sweeper_curve = value

    @property
    def mesh_points(self) -> ndarray:
        curve_fn = self.curve.get_path_fn()
        curve_np = self.num_points_curve
        curve_dm_fn = self.dist_curve.get_dist_fn()
        sweeper_fn = self.sweeper_curve.get_path_fn()
        sweeper_np = self.num_points_sweeper_curve
        sweeper_dm_fn = self.dist_sweeper_curve.get_dist_fn()
        mp = np.zeros((3, curve_np, sweeper_np))
        for i, u in enumerate(np.linspace(0, 1, num=curve_np, endpoint=True)):
            for j, w in enumerate(np.linspace(0, 1, num=sweeper_np, endpoint=True)):
                mp[:, i, j] = curve_fn(curve_dm_fn(u)) + sweeper_fn(sweeper_dm_fn(w))
        return mp
