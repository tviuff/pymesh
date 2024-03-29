"""Module containing the BilinearSurface class"""

from typing import Self

import numpy as np

from pymesh.descriptors import AsInstanceOf
from pymesh.geo.point import Point
from pymesh.geo.vector3d import Vector3D
from pymesh.geo.surfaces.surface import Surface
from pymesh.typing import NDArray3
from pymesh.utils import (
    validate_move_parameters,
    validate_rotate_parameters,
    validate_surface_path_parameters,
)


class BilinearSurface(Surface):
    """Creates a bilinear surface based on four points in space
    and creates mesh points for generating panels.
    """

    p00 = AsInstanceOf(Point)
    p10 = AsInstanceOf(Point)
    p01 = AsInstanceOf(Point)
    p11 = AsInstanceOf(Point)

    def __init__(self, p00: Point, p10: Point, p11: Point, p01: Point):
        """Creates a bilinear surface from the points p00, p10, p11 and p01.

        These four points represent the surface corners going counter-clockwise.
        The first number represents the value of u, while the second number
        represents the value of w.
        """
        self._all_surfaces.append(self)
        self.p00 = p00
        self.p10 = p10
        self.p11 = p11
        self.p01 = p01
        super().__init__()

    def path(
        self, u: int | float, w: int | float, uflip: bool = False, wflip: bool = False
    ) -> NDArray3[np.float64]:
        u, w = validate_surface_path_parameters(u, w, uflip, wflip)
        return (
            (1 - u) * w * self.p00.xyz
            + u * w * self.p10.xyz
            + (1 - u) * (1 - w) * self.p01.xyz
            + u * (1 - w) * self.p11.xyz
        )

    def get_max_lengths(self) -> tuple[float]:
        length_u_bottom = np.sqrt(np.sum((self.p00 - self.p10) ** 2))
        length_u_top = np.sqrt(np.sum((self.p01 - self.p11) ** 2))
        length_w_left = np.sqrt(np.sum((self.p00 - self.p01) ** 2))
        length_w_right = np.sqrt(np.sum((self.p10 - self.p11) ** 2))
        length_u = float(np.max((length_u_bottom, length_u_top)))
        length_w = float(np.max((length_w_left, length_w_right)))
        return length_u, length_w

    def copy(self) -> Self:
        return BilinearSurface(
            self.p00.copy(),
            self.p10.copy(),
            self.p11.copy(),
            self.p01.copy(),
        )

    def move(
        self, dx: int | float = 0.0, dy: int | float = 0.0, dz: int | float = 0.0
    ) -> None:
        validate_move_parameters(dx, dy, dz)
        self.p00.move(dx, dy, dz)
        self.p10.move(dx, dy, dz)
        self.p11.move(dx, dy, dz)
        self.p01.move(dx, dy, dz)

    def rotate(self, axis: Vector3D, angle: int | float) -> None:
        validate_rotate_parameters(axis, angle)
        self.p00.rotate(axis, angle)
        self.p10.rotate(axis, angle)
        self.p11.rotate(axis, angle)
        self.p01.rotate(axis, angle)
