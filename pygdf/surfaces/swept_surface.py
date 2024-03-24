"""Module including the swept surface class
"""

import numpy as np
from numpy import ndarray

from pygdf.constants import MeshConstants
from pygdf.curves.curve import Curve
from pygdf.descriptors import AsNumber, AsInstanceOf
from pygdf.mesh_distributions import MeshDistribution
from pygdf.surfaces.surface import Surface

class SweptSurface(Surface):
    """Creates a surface based on a curve swept by another
    and creates mesh points for generating panels.
    """

    boundary_distribution_curve = AsInstanceOf(MeshDistribution)
    boundary_distribution_sweeper_curve = AsInstanceOf(MeshDistribution)
    panel_density_curve = AsNumber(minvalue=0)
    panel_density_sweeper_curve = AsNumber(minvalue=0)

    def __init__(self, curve:Curve, sweeper_curve:Curve):
        self._all_surfaces.append(self)
        self.curve = curve
        self.sweeper_curve = sweeper_curve
        self.boundary_distribution_curve = MeshConstants.DEFAULT_DIST_METHOD.value()
        self.boundary_distribution_sweeper_curve = MeshConstants.DEFAULT_DIST_METHOD.value()
        self.panel_density_curve = MeshConstants.DEFAULT_DENSITY.value
        self.panel_density_sweeper_curve = MeshConstants.DEFAULT_DENSITY.value

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

    def _get_num_points(self) -> tuple[int]:
        density_curve = self.panel_density_curve
        density_sweeper = self.panel_density_sweeper_curve
        num_points_curve = density_curve + 1
        num_points_sweeper = density_sweeper + 1
        if isinstance(density_curve, float) or isinstance(density_sweeper, float):
            length_curve = self.curve.length
            length_sweeper = self.sweeper_curve.length
            if isinstance(density_curve, float):
                num_points_curve = int(np.ceil(length_curve / density_curve) + 1)
            if isinstance(density_sweeper, float):
                num_points_sweeper = int(np.ceil(length_sweeper / density_sweeper) + 1)
        return num_points_curve, num_points_sweeper

    @property
    def mesh_points(self) -> ndarray:
        np_curve, np_sweeper = self._get_num_points()
        curve_path = self.curve.get_path_fn()
        sweeper_path = self.sweeper_curve.get_path_fn()
        dist_curve = self.boundary_distribution_curve.get_dist_fn()
        dist_sweeper = self.boundary_distribution_sweeper_curve.get_dist_fn()
        mp = np.zeros((3, np_curve, np_sweeper))
        for i, u in enumerate(np.linspace(0, 1, num=np_curve, endpoint=True)):
            for j, w in enumerate(np.linspace(0, 1, num=np_sweeper, endpoint=True)):
                mp[:, i, j] = curve_path(dist_curve(u)) + sweeper_path(dist_sweeper(w))
        return mp
