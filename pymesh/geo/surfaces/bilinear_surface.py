"""Module including the bilinear surface class
"""

from typing import Self

import numpy as np

from pymesh.descriptors import AsNDArray
from pymesh.geo.point import Point
from pymesh.geo.surfaces.surface import Surface
from pymesh.mesh.mesh_generator import MeshGenerator
from pymesh.typing import NDArray3
from pymesh.utils import validate_move_parameters, validate_surface_path_parameters

# ! use point name convention point00, point01, point10 and point11


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
        bottom_left: Point,
        bottom_right: Point,
        top_right: Point,
        top_left: Point,
    ):
        self._all_surfaces.append(self)
        self.bottom_left = bottom_left.xyz
        self.bottom_right = bottom_right.xyz
        self.top_right = top_right.xyz
        self.top_left = top_left.xyz
        self._set_mesh_generator(
            MeshGenerator(self.get_path(), self.get_max_lengths()), force=True
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

    def copy(self) -> Self:
        bottom_left = Point(
            self.bottom_left[0], self.bottom_left[1], self.bottom_left[2]
        )
        bottom_right = Point(
            self.bottom_right[0], self.bottom_right[1], self.bottom_right[2]
        )
        top_right = Point(self.top_right[0], self.top_right[1], self.top_right[2])
        top_left = Point(self.top_left[0], self.top_left[1], self.top_left[2])
        return BilinearSurface(bottom_left, bottom_right, top_right, top_left)

    def move(
        self, dx: int | float = 0.0, dy: int | float = 0.0, dz: int | float = 0.0
    ) -> None:
        validate_move_parameters(dx, dy, dz)
        dxyz = np.array([dx, dy, dz])
        self.bottom_left += dxyz
        self.bottom_right += dxyz
        self.top_right += dxyz
        self.top_left += dxyz
