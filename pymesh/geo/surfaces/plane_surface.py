"""Module including the plane surface class
"""

from typing import Self

import numpy as np

from pymesh.descriptors import AsNDArray
from pymesh.geo.point import Point
from pymesh.geo.surfaces.surface import Surface
from pymesh.mesh.mesh_generator import MeshGenerator
from pymesh.typing import NDArray3
from pymesh.utils import validate_move_parameters, validate_surface_path_parameters


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
            MeshGenerator(self.get_path(), self.get_max_lengths()), force=True
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

    def copy(self) -> Self:
        point_0 = Point(self.point_0[0], self.point_0[1], self.point_0[2])
        point_1 = self.vector_01 + self.point_0
        point_1 = Point(point_1[0], point_1[1], point_1[2])
        point_2 = self.vector_02 + self.point_0
        point_2 = Point(point_2[0], point_2[1], point_2[2])
        return PlaneSurface(point_0, point_1, point_2)

    def move(
        self, dx: int | float = 0.0, dy: int | float = 0.0, dz: int | float = 0.0
    ) -> None:
        validate_move_parameters(dx, dy, dz)
        dxyz = np.array([dx, dy, dz])
        self.point_0 += dxyz  # vectors are relative to point_0
