"""Module including the plane surface class
"""

import numpy as np

from pymesh.geo.point import Point
from pymesh.utils.typing import NDArray3, NDArray3xNxN
from pymesh.utils.descriptors import AsInstanceOf
from pymesh.mesh.surface_mesh_generator import SurfaceMeshGenerator
from pymesh.geo.surfaces.surface import Surface, validate_path_parameters


class PlaneSurface(Surface):
    """Creates a plane surface based on three points in space
    and creates mesh points for generating panels.
    """

    point_0 = AsInstanceOf(Point)
    point_1 = AsInstanceOf(Point)
    point_2 = AsInstanceOf(Point)

    def __init__(self, point_0: Point, point_1: Point, point_2: Point):
        self._all_surfaces.append(self)
        self.point_0 = point_0
        self.point_1 = point_1
        self.point_2 = point_2
        self._set_mesh_generator(
            SurfaceMeshGenerator(self.get_path(), self.get_max_lengths()), force=True
        )

    def path(self, u: int | float, w: int | float) -> NDArray3[np.float64]:
        u, w = validate_path_parameters(u, w)
        pu = self.point_0.xyz + (self.point_1.xyz - self.point_0.xyz) * u
        pw = self.point_0.xyz + (self.point_2.xyz - self.point_0.xyz) * w
        return pu + pw

    def get_max_lengths(self) -> tuple[float]:
        length_01 = float(np.sqrt(np.sum((self.point_1.xyz - self.point_0.xyz) ** 2)))
        length_02 = float(np.sqrt(np.sum((self.point_2.xyz - self.point_0.xyz) ** 2)))
        return length_01, length_02

    @property
    def mesh_points(self) -> NDArray3xNxN[np.float64]:
        return self.mesher.generate_mesh_points()
