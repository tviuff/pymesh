"""Module containing the PlaneSurface class"""

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


class PlaneSurface(Surface):
    """Creates a plane surface based on three points in space
    and creates mesh points for generating panels.
    """

    point0 = AsInstanceOf(Point)
    point1 = AsInstanceOf(Point)
    point2 = AsInstanceOf(Point)

    def __init__(self, point0: Point, point1: Point, point2: Point):
        """Creates a plane surface from three points in space.

        The plane is drawn from the vectors |point1-poin0| and
        |point2-poin0|, where point0 is shared between the vectors.
        """
        self._all_surfaces.append(self)
        self.point0 = point0
        self.point1 = point1
        self.point2 = point2
        super().__init__()

    def path(
        self, u: int | float, w: int | float, uflip: bool = False, wflip: bool = False
    ) -> NDArray3[np.float64]:
        # ! find a way to add np.ndarray to Point using __add__
        u, w = validate_surface_path_parameters(u, w, uflip, wflip)
        xyz0 = self.point0.xyz
        u_point = (self.point1 - self.point0) * u
        w_point = (self.point2 - self.point0) * w
        return xyz0 + u_point + w_point

    def get_max_lengths(self) -> tuple[float]:
        length_u = float(np.sqrt(np.sum((self.point1 - self.point0) ** 2)))
        length_w = float(np.sqrt(np.sum((self.point2 - self.point0) ** 2)))
        return length_u, length_w

    def shallowcopy(self) -> Self:
        return PlaneSurface(self.point0, self.point1, self.point2)

    def deepcopy(self) -> Self:
        return PlaneSurface(
            self.point0.deepcopy(), self.point1.deepcopy(), self.point2.deepcopy()
        )

    def move(
        self, dx: int | float = 0.0, dy: int | float = 0.0, dz: int | float = 0.0
    ) -> None:
        validate_move_parameters(dx, dy, dz)
        self.point0.move(dx, dy, dz)
        self.point1.move(dx, dy, dz)
        self.point2.move(dx, dy, dz)

    def rotate(self, axis: Vector3D, angle: int | float) -> None:
        validate_rotate_parameters(axis, angle)
        self.point0.rotate(axis, angle)
        self.point1.rotate(axis, angle)
        self.point2.rotate(axis, angle)
