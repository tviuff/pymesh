"""Module including the plane surface class
"""

import numpy as np

from pymesh.geo.point import Point
from pymesh.utils.typing import NDArray3
from pymesh.utils.descriptors import AsInstanceOf, AsNDArray
from pymesh.mesh.surface_mesh_generator import SurfaceMeshGenerator
from pymesh.geo.surfaces.surface import Surface, validate_surface_path_parameters


class PlaneSurface(Surface):
    """Creates a plane surface based on three points in space
    and creates mesh points for generating panels.
    """

    point_0 = AsNDArray(shape=(3,))
    vector_01 = AsNDArray(shape=(3,))
    vector_02 = AsNDArray(shape=(3,))

    def __init__(self, point_0: Point, point_1: Point, point_2: Point):
        self._all_surfaces.append(self)
        self.point_0 = point_0.xyz
        self.vector_01 = point_1.xyz - point_0.xyz
        self.vector_02 = point_2.xyz - point_0.xyz
        self._set_mesh_generator(
            SurfaceMeshGenerator(self.get_path(), self.get_max_lengths()), force=True
        )

    def path(
        self, u: int | float, w: int | float, uflip: bool = False, wflip: bool = False
    ) -> NDArray3[np.float64]:
        u, w = validate_surface_path_parameters(u, w, uflip, wflip)
        pu = self.point_0 + self.vector_01 * u
        pw = self.point_0 + self.vector_02 * w
        return pu + pw

    def get_max_lengths(self) -> tuple[float]:
        length_01 = float(np.sqrt(np.sum(self.vector_01**2)))
        length_02 = float(np.sqrt(np.sum(self.vector_02**2)))
        return length_01, length_02
