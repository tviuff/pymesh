"""Module including the bilinear surface class
"""

import numpy as np

from pymesh.geo.point import Point
from pymesh.utils.typing import NDArray3, NDArray3xNxN
from pymesh.utils.descriptors import AsInstanceOf
from pymesh.mesh.surface_mesh_generator import SurfaceMeshGenerator
from pymesh.geo.surfaces.surface import Surface, validate_path_parameters


class BilinearSurface(Surface):
    """Creates a bilinear surface based on four points in space
    and creates mesh points for generating panels.
    """

    point_bottom_left = AsInstanceOf(Point)
    point_bottom_right = AsInstanceOf(Point)
    point_top_left = AsInstanceOf(Point)
    point_top_right = AsInstanceOf(Point)

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
        self._set_mesh_generator(
            SurfaceMeshGenerator(self.get_path(), self.get_max_lengths()), force=True
        )

    def path(self, u: int | float, w: int | float) -> NDArray3[np.float64]:
        u, w = validate_path_parameters(u, w)
        return (
            (1 - u) * w * self.point_bottom_left.xyz
            + u * w * self.point_bottom_right.xyz
            + (1 - u) * (1 - w) * self.point_top_left.xyz
            + u * (1 - w) * self.point_top_right.xyz
        )

    def get_max_lengths(self) -> tuple[float]:
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
            np.max((length_left_right_bottom, length_left_right_top))
        )
        length_top_bottom = float(
            np.max((length_top_bottom_left, length_top_bottom_right))
        )
        return length_top_bottom, length_left_right

    @property
    def mesh_points(self) -> NDArray3xNxN[np.float64]:
        return self.mesher.generate_mesh_points()
