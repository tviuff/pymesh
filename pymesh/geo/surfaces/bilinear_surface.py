"""Module including the bilinear surface class
"""

import numpy as np

from pymesh.geo.point import Point
from pymesh.typing import NDArray3
from pymesh.descriptors import AsNDArray
from pymesh.mesh.surface_mesh_generator import SurfaceMeshGenerator
from pymesh.geo.surfaces.surface import Surface, validate_surface_path_parameters


class BilinearSurface(Surface):
    """Creates a bilinear surface based on four points in space
    and creates mesh points for generating panels.
    """

    bottom_left = AsNDArray(shape=(3,))
    bottom_right = AsNDArray(shape=(3,))
    top_left = AsNDArray(shape=(3,))
    top_right = AsNDArray(shape=(3,))

    def __init__(
        self,
        point_bottom_left: Point,
        point_bottom_right: Point,
        point_top_right: Point,
        point_top_left: Point,
    ):
        self._all_surfaces.append(self)
        self.bottom_left = point_bottom_left.xyz
        self.bottom_right = point_bottom_right.xyz
        self.top_right = point_top_right.xyz
        self.top_left = point_top_left.xyz
        self._set_mesh_generator(
            SurfaceMeshGenerator(self.get_path(), self.get_max_lengths()), force=True
        )

    def path(
        self, u: int | float, w: int | float, uflip: bool = False, wflip: bool = False
    ) -> NDArray3[np.float64]:
        u, w = validate_surface_path_parameters(u, w, uflip, wflip)
        return (
            (1 - u) * w * self.bottom_left
            + u * w * self.bottom_right
            + (1 - u) * (1 - w) * self.top_left
            + u * (1 - w) * self.top_right
        )

    def get_max_lengths(self) -> tuple[float]:
        length_left_right_bottom = np.sqrt(
            np.sum((self.bottom_left - self.bottom_right) ** 2)
        )
        length_left_right_top = np.sqrt(np.sum((self.top_left - self.top_right) ** 2))
        length_top_bottom_left = np.sqrt(
            np.sum((self.bottom_left - self.top_left) ** 2)
        )
        length_top_bottom_right = np.sqrt(
            np.sum((self.bottom_right - self.top_right) ** 2)
        )
        length_left_right = float(
            np.max((length_left_right_bottom, length_left_right_top))
        )
        length_top_bottom = float(
            np.max((length_top_bottom_left, length_top_bottom_right))
        )
        return length_top_bottom, length_left_right
