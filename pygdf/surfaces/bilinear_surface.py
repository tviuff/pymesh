"""Module including the bilinear surface class
"""

import numpy as np

from pygdf.auxiliary.point import Point
from pygdf.constants import MeshConstants
from pygdf.descriptors import AsNumber, AsInstanceOf
from pygdf.mesh_distributions import MeshDistribution
from pygdf.surfaces.surface import Surface


class BilinearSurface(Surface):
    """Creates a bilinear surface based on four points in space
    and creates mesh points for generating panels.
    """

    point_bottom_left = AsInstanceOf(Point)
    point_bottom_right = AsInstanceOf(Point)
    point_top_left = AsInstanceOf(Point)
    point_top_right = AsInstanceOf(Point)
    distribution_top_bottom = AsInstanceOf(MeshDistribution)
    distribution_left_right = AsInstanceOf(MeshDistribution)
    panel_density_top_bottom = AsNumber(minvalue=0)
    panel_density_left_right = AsNumber(minvalue=0)

    def __init__(
        self,
        point_bottom_left: Point,
        point_bottom_right: Point,
        point_top_right: Point,
        point_top_left: Point,
    ):
        self._all_surfaces.append(self)
        self.point_bottom_left = point_bottom_left
        self.point_bottom_right = point_bottom_right
        self.point_top_right = point_top_right
        self.point_top_left = point_top_left
        self.distribution_top_bottom = MeshConstants.DEFAULT_DISTRIBUTION_METHOD.value()
        self.distribution_left_right = MeshConstants.DEFAULT_DISTRIBUTION_METHOD.value()
        self.panel_density_top_bottom = MeshConstants.DEFAULT_DENSITY.value
        self.panel_density_left_right = MeshConstants.DEFAULT_DENSITY.value

    def _get_lengths(self) -> tuple[float]:
        length_left_right_bottom = np.sqrt(
            np.sum((self.point_bottom_left.xyz - self.point_bottom_right.xyz) ** 2)
        )
        length_left_right_top = np.sqrt(
            np.sum((self.point_top_left.xyz - self.point_top_right.xyz) ** 2)
        )
        length_top_bottom_left = np.sqrt(
            np.sum((self.point_bottom_left.xyz - self.point_top_left.xyz) ** 2)
        )
        length_top_bottom_right = np.sqrt(
            np.sum((self.point_bottom_right.xyz - self.point_top_right.xyz) ** 2)
        )
        length_left_right = float(
            np.max(length_left_right_bottom, length_left_right_top)
        )
        length_top_bottom = float(
            np.max(length_top_bottom_left, length_top_bottom_right)
        )
        return length_top_bottom, length_left_right

    def _get_num_points(self) -> tuple[int]:
        density_top_bottom = self.panel_density_top_bottom
        density_left_right = self.panel_density_left_right
        num_points_top_bottom = density_top_bottom + 1
        num_points_left_right = density_left_right + 1
        if isinstance(density_top_bottom, float) or isinstance(
            density_left_right, float
        ):
            length_top_bottom, length_left_right = self._get_lengths()
            if isinstance(density_top_bottom, float):
                num_points_top_bottom = int(
                    np.ceil(length_top_bottom / density_top_bottom) + 1
                )
            if isinstance(density_left_right, float):
                num_points_left_right = int(
                    np.ceil(length_left_right / density_left_right) + 1
                )
        return num_points_top_bottom, num_points_left_right

    @property
    def mesh_points(self) -> np.ndarray:
        np_top_bottom, np_left_right = self._get_num_points()
        dist_tb = self.distribution_top_bottom.get_dist_fn()
        dist_lr = self.distribution_left_right.get_dist_fn()
        mp = np.zeros((3, np_left_right, np_top_bottom))
        for i, u in enumerate(np.linspace(0, 1, num=np_left_right, endpoint=True)):
            for j, w in enumerate(np.linspace(0, 1, num=np_top_bottom, endpoint=True)):
                mp[:, i, j] = (
                    0
                    + (1 - dist_lr(u)) * dist_tb(w) * self.point_bottom_left.xyz
                    + dist_lr(u) * dist_tb(w) * self.point_bottom_right.xyz
                    + (1 - dist_lr(u)) * (1 - dist_tb(w)) * self.point_top_left.xyz
                    + dist_lr(u) * (1 - dist_tb(w)) * self.point_top_right.xyz
                )
        return mp
