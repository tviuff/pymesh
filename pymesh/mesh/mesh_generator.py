"""Module containing MeshGenerator class"""

import numpy as np

from pymesh.geo.surfaces.surface import Surface

# from pymesh.constants import MeshConstants
# from pymesh.descriptors import AsContainerOf
from pymesh.mesh.mesh_distributions import MeshDistribution, LinearDistribution
from pymesh.typing import NDArray3xNxN


# LENGTH: int = 2
# NUM: int = 100


class MeshGenerator:
    """Surface mesh generator"""

    surfaces: list = []

    def add_surface(
        self,
        surface: Surface,
        density_u: int | float = 0.2,
        density_w: int | float = 0.2,
        distribution_u: MeshDistribution = LinearDistribution(),
        distribution_w: MeshDistribution = LinearDistribution(),
    ) -> None:
        length_u, length_w = surface.get_max_lengths()
        num_points_u = self.get_num_points(length_u, density_u)
        num_points_w = self.get_num_points(length_w, density_w)
        data = {
            "path": surface.get_path(),
            "flipped_normal": surface.is_normal_flipped,
            "num_points": (num_points_u, num_points_w),
            "distributions": (distribution_u, distribution_w),
        }
        self.surfaces.append(data)

    @staticmethod
    def get_num_points(length, density) -> tuple[int]:
        """Returns number of points along a dimension"""
        num_points = density + 1
        if isinstance(density, float):
            num_points = int(np.ceil(length / density) + 1)
        return num_points

    @staticmethod
    def _generate_mesh_points(mesh) -> NDArray3xNxN[np.float64]:
        """Generates mesh points"""
        path = mesh["path"]
        num_points_u, num_points_w = mesh["num_points"]
        distribution_u, distribution_w = mesh["distributions"]
        ufn = distribution_u.get_dist_fn()
        wfn = distribution_w.get_dist_fn()
        mp = np.zeros((3, num_points_u, num_points_w))
        for i, u in enumerate(np.linspace(0, 1, num=num_points_u, endpoint=True)):
            for j, w in enumerate(np.linspace(0, 1, num=num_points_w, endpoint=True)):
                mp[:, i, j] = path(ufn(u), wfn(w))
        return mp

    @staticmethod
    def _generate_panels(
        mesh_points: NDArray3xNxN[np.float64], flipped_normal: bool
    ) -> list[list[float]]:
        """Returns list of quadrilateral panels.

        Each panel is defined as a list of 12 floating numbers,
        representing the xyz coordinates of the four panel vertices:
        panel = [x0, y0, z0, x1, y1, z1, x2, y2, z2, x3, y3, z3]
        """
        panels = []
        mp = mesh_points
        for j in range(0, mp.shape[2] - 1):
            for i in range(0, mp.shape[1] - 1):
                xyz1 = mp[:, i, j]
                xyz2 = mp[:, i + 1, j]
                xyz3 = mp[:, i + 1, j + 1]
                xyz4 = mp[:, i, j + 1]
                if flipped_normal:
                    xyz1, xyz2, xyz3, xyz4 = xyz4, xyz3, xyz2, xyz1
                panels.append(
                    [
                        xyz1[0],
                        xyz1[1],
                        xyz1[2],
                        xyz2[0],
                        xyz2[1],
                        xyz2[2],
                        xyz3[0],
                        xyz3[1],
                        xyz3[2],
                        xyz4[0],
                        xyz4[1],
                        xyz4[2],
                    ]
                )
        return panels

    def get_panels(self):
        """Loops through mesh_surfaces and returns generated panels"""
        panels = []
        for data in self.surfaces:
            mesh_points = self._generate_mesh_points(data)
            surface_panels = self._generate_panels(mesh_points, data["flipped_normal"])
            panels += surface_panels
        return panels
