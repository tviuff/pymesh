"""Module including the ruled surface class
"""

import numpy as np
from numpy import ndarray

from pygdf.constants import MeshConstants
from pygdf.curves.curve import Curve
from pygdf.descriptors import AsNumber, AsInstanceOf
from pygdf.mesh_distributions import MeshDistribution
from pygdf.surfaces.surface import Surface

# ! Consider using a combination of .length and .get_path_fn() to avoid coupling


class RuledSurface(Surface):
    """Creates a ruled surface based on two curves
    and creates mesh points for generating panels.
    """

    boundary_distribution_curves = AsInstanceOf(MeshDistribution)
    boundary_distribution_in_between = AsInstanceOf(MeshDistribution)
    panel_density_curves = AsNumber(minvalue=0)
    panel_density_in_between = AsNumber(minvalue=0)

    def __init__(self, curve_1: Curve, curve_2: Curve):
        self._all_surfaces.append(self)
        self.curve_1 = curve_1
        self.curve_2 = curve_2
        self.boundary_distribution_curves = (
            MeshConstants.DEFAULT_DISTRIBUTION_METHOD.value()
        )
        self.boundary_distribution_in_between = (
            MeshConstants.DEFAULT_DISTRIBUTION_METHOD.value()
        )
        self.panel_density_curves = MeshConstants.DEFAULT_DENSITY.value
        self.panel_density_in_between = MeshConstants.DEFAULT_DENSITY.value

    @property
    def curve_1(self) -> Curve:
        return self._curve_1

    @curve_1.setter
    def curve_1(self, value) -> None:
        if not isinstance(value, Curve):
            raise TypeError("curve_1 must be of type 'Curve'")
        self._curve_1 = value

    @property
    def curve_2(self) -> Curve:
        return self._curve_2

    @curve_2.setter
    def curve_2(self, value) -> None:
        if not isinstance(value, Curve):
            raise TypeError("curve_2 must be of type 'Curve'")
        self._curve_2 = value

    def _get_lengths(self) -> tuple[float]:
        """Returns largest boundary length along two dimensions.

        1) largest distance along curve paths.
        2) largest distance between opposing curves end points.
        """
        length_1 = max(self.curve_1.length, self.curve_2.length)
        start_points = (self.curve_1.point_start.xyz, self.curve_2.point_start.xyz)
        end_points = (self.curve_1.point_end.xyz, self.curve_2.point_end.xyz)
        length_2_start = float(
            np.sqrt(np.sum((start_points[0] - start_points[1]) ** 2))
        )
        length_2_end = float(np.sqrt(np.sum((end_points[0] - end_points[1]) ** 2)))
        length_2 = max(length_2_start, length_2_end)
        return length_1, length_2

    def _get_num_points(self) -> tuple[int]:
        density_1, density_2 = self.panel_density_curves, self.panel_density_in_between
        num_points_1 = density_1 + 1
        num_points_2 = density_2 + 1
        if isinstance(density_1, float) or isinstance(density_2, float):
            length_1, length_2 = self._get_lengths()
            if isinstance(density_1, float):
                num_points_1 = int(np.ceil(length_1 / density_1) + 1)
            if isinstance(density_2, float):
                num_points_2 = int(np.ceil(length_2 / density_2) + 1)
        return num_points_1, num_points_2

    @property
    def mesh_points(self) -> ndarray:
        np_curves, np_in_between = self._get_num_points()
        curve_fn_1 = self.curve_1.get_path_fn()
        curve_fn_2 = self.curve_2.get_path_fn()
        dist_curves = self.boundary_distribution_curves.get_dist_fn()
        dist_in_between = self.boundary_distribution_in_between.get_dist_fn()
        mp = np.zeros((3, np_curves, np_in_between))
        for i, u in enumerate(np.linspace(0, 1, num=np_curves, endpoint=True)):
            for j, w in enumerate(np.linspace(0, 1, num=np_in_between, endpoint=True)):
                mp[:, i, j] = (
                    0
                    + (1 - dist_in_between(w)) * curve_fn_1(dist_curves(u))
                    + dist_in_between(w) * curve_fn_2(dist_curves(u))
                )
        return mp
