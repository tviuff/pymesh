"""Module containing surface mesher class"""

from collections.abc import Callable

import numpy as np

from pymesh.utils.constants import MeshConstants
from pymesh.utils.descriptors import AsContainerOf
from pymesh.mesh.distributions import MeshDistribution
from pymesh.utils.typing import NDArray3xNxN


LENGTH: int = 2
NUM: int = 100


class SurfaceMeshGenerator:
    """Surface mesh generator"""

    mesh_distributions = AsContainerOf(
        container_type=tuple,
        item_type=MeshDistribution,
        min_length=LENGTH,
        max_length=LENGTH,
    )
    panel_densities = AsContainerOf(
        container_type=tuple,
        item_type=int | float,
        min_length=LENGTH,
        max_length=LENGTH,
    )
    lengths = AsContainerOf(
        container_type=tuple, item_type=float, min_length=LENGTH, max_length=LENGTH
    )

    def __init__(
        self,
        surface_fn: Callable[[int | float, int | float], NDArray3xNxN[np.float64]],
        lengths: tuple[float],
    ):
        self.surface_fn = surface_fn
        self.lengths = lengths
        self.mesh_distributions = (
            MeshConstants.DEFAULT_DISTRIBUTION_METHOD.value(),
            MeshConstants.DEFAULT_DISTRIBUTION_METHOD.value(),
        )
        self.panel_densities = (
            MeshConstants.DEFAULT_DENSITY.value,
            MeshConstants.DEFAULT_DENSITY.value,
        )

    def set_u_parameters(
        self, panel_density: int | float = None, distribution: MeshDistribution = None
    ) -> None:
        """Sets surface mesh parameters for the u dimension"""
        index = 0
        if panel_density is not None:
            self._set_panel_density_index(panel_density, index)
        if distribution is not None:
            self._set_mesh_distribution_index(distribution, index)

    def set_w_parameters(
        self, panel_density: int | float = None, distribution: MeshDistribution = None
    ) -> None:
        """Sets surface mesh parameters for the w dimension"""
        index = 1
        if panel_density is not None:
            self._set_panel_density_index(panel_density, index)
        if distribution is not None:
            self._set_mesh_distribution_index(distribution, index)

    def _set_panel_density_index(self, value: int | float, index: int) -> None:
        if not isinstance(index, int):
            raise TypeError(f"Expected {index!r} to be an int.")
        if index not in [0, 1]:
            raise TypeError(f"Expected {index!r} to be either 0 or 1.")
        densities = list(self.panel_densities)
        densities[index] = value
        self.panel_densities = tuple(densities)

    def _set_mesh_distribution_index(self, value: int | float, index: int) -> None:
        if not isinstance(index, int):
            raise TypeError(f"Expected {index!r} to be an int.")
        if index not in [0, 1]:
            raise TypeError(f"Expected {index!r} to be either 0 or 1.")
        distributions = list(self.mesh_distributions)
        distributions[index] = value
        self.mesh_distributions = tuple(distributions)

    def get_approximate_lengths(self, num: int = NUM):
        """Returns the largest boundary lengths based on a linear path
        discretization algorithm based on num points along the path."""
        # ! Not yet tested
        arr_u = np.zeros((2, num))
        arr_w = np.zeros((2, num))
        for i in np.linspace(0, 1, num=num, endpoint=True):
            arr_u[0, i] = self.surface_fn(u=i, w=0)
            arr_u[1, i] = self.surface_fn(u=i, w=1)
            arr_w[0, i] = self.surface_fn(u=0, w=i)
            arr_w[1, i] = self.surface_fn(u=1, w=i)
        length_u = np.max(np.sum(np.diff(arr_u, axis=1), axis=1), axis=0)
        length_w = np.max(np.sum(np.diff(arr_w, axis=1), axis=1), axis=0)
        return (length_u, length_w)

    def get_num_points(self) -> tuple[int]:
        """Returns number of points along the u and w dimensions"""
        density_u, density_w = self.panel_densities
        num_points_u = density_u + 1
        num_points_w = density_w + 1
        if isinstance(density_u, float) or isinstance(density_w, float):
            length_u, length_w = self.lengths
            if isinstance(density_u, float):
                num_points_u = int(np.ceil(length_u / density_u) + 1)
            if isinstance(density_w, float):
                num_points_w = int(np.ceil(length_w / density_w) + 1)
        return num_points_u, num_points_w

    def generate_mesh_points(self) -> NDArray3xNxN[np.float64]:
        """Generates 3-dimensional surface mesh points."""
        num_points_u, num_points_w = self.get_num_points()
        distribution_u, distribution_w = self.mesh_distributions
        ufn = distribution_u.get_dist_fn()
        wfn = distribution_w.get_dist_fn()
        mp = np.zeros((3, num_points_u, num_points_w))
        for i, u in enumerate(np.linspace(0, 1, num=num_points_u, endpoint=True)):
            for j, w in enumerate(np.linspace(0, 1, num=num_points_w, endpoint=True)):
                mp[:, i, j] = self.surface_fn(ufn(u), wfn(w))
        return mp
