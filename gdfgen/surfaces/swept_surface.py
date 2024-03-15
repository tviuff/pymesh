"""Module including the swept surface class
"""

import numpy as np
from numpy import ndarray

from gdfgen.constants import MeshConstants
from gdfgen.curves import Curve
from gdfgen.mesh import BoundaryDistribution, MeshNumber
from gdfgen.surfaces import Surface

class SweptSurface(Surface):
    """Creates a surface based on a curve swept by another
    and creates mesh points for generating panels.
    """

    dist_curve = BoundaryDistribution()
    dist_sweeper_curve = BoundaryDistribution()
    num_points_curve = MeshNumber()
    num_points_sweeper_curve = MeshNumber()

    def __init__(self, curve:Curve, sweeper_curve:Curve):
        self.curve = curve
        self.sweeper_curve = sweeper_curve
        self.dist_curve = MeshConstants.DEFAULT_DIST_METHOD.value
        self.dist_sweeper_curve = MeshConstants.DEFAULT_DIST_METHOD.value
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
        xyz_curve = self.curve.get_path_xyz(
            num_points = self.num_points_curve,
            dist_method = self.dist_curve
            )
        xyz_sweeper_curve = self.sweeper_curve.get_path_xyz(
            num_points = self.num_points_sweeper_curve,
            dist_method = self.dist_sweeper_curve
            )
        mp = np.zeros((3, self.num_points_curve, self.num_points_sweeper_curve))
        for i in range(0, self.num_points_curve):
            for j in range(0, self.num_points_sweeper_curve):
                for k in range(0, 3):
                    mp[k, i, j] = xyz_curve[i, k] + xyz_sweeper_curve[j, k]
        self._mesh_points = mp
        return self._mesh_points
