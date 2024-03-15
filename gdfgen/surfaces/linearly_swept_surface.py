"""Module including the linearly swept surface class
"""

import numpy as np
from numpy import ndarray

from gdfgen import Line
from gdfgen.constants import MeshConstants
from gdfgen.curves import Curve
from gdfgen.mesh import BoundaryDistribution, MeshNumber
from gdfgen.surfaces import Surface

class LinearlySweptSurface(Surface):
    """Creates a surface based on a curve swept by a line
    and creates mesh points for generating panels.
    """

    dist_curve = BoundaryDistribution()
    dist_line = BoundaryDistribution()
    num_points_curve = MeshNumber()
    num_points_line = MeshNumber()

    def __init__(self, curve:Curve, line:Line):
        self.curve = curve
        self.line = line
        self.dist_curve = MeshConstants.DEFAULT_DIST_METHOD.value
        self.dist_line = MeshConstants.DEFAULT_DIST_METHOD.value
        self.num_points_curve = MeshConstants.DEFAULT_NUM_POINT.value
        self.num_points_line = MeshConstants.DEFAULT_NUM_POINT.value

    @property
    def curve(self)-> Curve:
        return self._curve

    @curve.setter
    def curve(self, curve:Curve) -> None:
        if not isinstance(curve, Curve):
            raise TypeError("curve must be of type 'Curve'.")
        self._curve = curve

    @property
    def line(self)-> Line:
        return self._line

    @line.setter
    def line(self, value:Line) -> None:
        if not isinstance(value, Line):
            raise TypeError("line must be of type 'Line'.")
        self._line = value

    @property
    def mesh_points(self) -> ndarray:
        xyz_curve = self.curve.get_path_xyz(
            num_points = self.num_points_curve,
            dist_method = self.dist_curve
            )
        xyz_line = self.line.get_path_xyz(
            num_points = self.num_points_line,
            dist_method = self.dist_line
            )
        mp = np.zeros((3, self.num_points_curve, self.num_points_line))
        for i in range(0, self.num_points_curve):
            for j in range(0, self.num_points_line):
                for k in range(0, 3):
                    mp[k, i, j] = xyz_curve[i, k] + xyz_line[j, k]
        self._mesh_points = mp
        return self._mesh_points
