"""Module including the plane surface class
"""

import numpy as np
from numpy import ndarray

from pygdf.auxiliary.point import Point
from pygdf.constants import MeshConstants
from pygdf.descriptors import AsNumber, AsInstanceOf
from pygdf.mesh_distributions import MeshDistribution
from pygdf.surfaces.surface import Surface


class PlaneSurface(Surface):
    """Creates a plane surface based on three points in space
    and creates mesh points for generating panels.
    """

    point_0 = AsInstanceOf(Point)
    point_1 = AsInstanceOf(Point)
    point_2 = AsInstanceOf(Point)
    boundary_distribution_01 = AsInstanceOf(MeshDistribution)
    boundary_distribution_02 = AsInstanceOf(MeshDistribution)
    panel_density_01 = AsNumber(minvalue=0)
    panel_density_02 = AsNumber(minvalue=0)

    def __init__(self, point_0: Point, point_1: Point, point_2: Point):
        self._all_surfaces.append(self)
        self.point_0 = point_0
        self.point_1 = point_1
        self.point_2 = point_2
        self.boundary_distribution_01 = (
            MeshConstants.DEFAULT_DISTRIBUTION_METHOD.value()
        )
        self.boundary_distribution_02 = (
            MeshConstants.DEFAULT_DISTRIBUTION_METHOD.value()
        )
        self.panel_density_01 = MeshConstants.DEFAULT_DENSITY.value
        self.panel_density_02 = MeshConstants.DEFAULT_DENSITY.value

    def _get_num_points(self) -> tuple[int]:
        density_01, density_02 = self.panel_density_01, self.panel_density_02
        num_points_01 = density_01 + 1
        num_points_02 = density_02 + 1
        if isinstance(density_01, float) or isinstance(density_02, float):
            length_01 = float(
                np.sqrt(np.sum((self.point_1.xyz - self.point_0.xyz) ** 2))
            )
            length_02 = float(
                np.sqrt(np.sum((self.point_2.xyz - self.point_0.xyz) ** 2))
            )
            if isinstance(density_01, float):
                num_points_01 = int(np.ceil(length_01 / density_01) + 1)
            if isinstance(density_02, float):
                num_points_02 = int(np.ceil(length_02 / density_02) + 1)
        return num_points_01, num_points_02

    @property
    def mesh_points(self) -> ndarray:

        def line1(u):
            fn = self.boundary_distribution_01.get_dist_fn()
            return self.point_0.xyz + (self.point_1.xyz - self.point_0.xyz) * fn(u)

        def line2(u):
            fn = self.boundary_distribution_02.get_dist_fn()
            return self.point_0.xyz + (self.point_2.xyz - self.point_0.xyz) * fn(u)

        num_points_01, num_points_02 = self._get_num_points()
        mp = np.zeros((3, num_points_01, num_points_02))
        for i, u in enumerate(np.linspace(0, 1, num=num_points_01, endpoint=True)):
            for j, w in enumerate(np.linspace(0, 1, num=num_points_02, endpoint=True)):
                mp[:, i, j] = line1(u) + line2(w)
        return mp
