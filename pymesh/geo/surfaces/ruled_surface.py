"""Module containing the ruled RuledSurface class"""

from typing import Self

import numpy as np

from pymesh.descriptors import AsInstanceOf
from pymesh.geo.curves.curve import Curve
from pymesh.geo.surfaces.surface import Surface
from pymesh.geo.vector3d import Vector3D
from pymesh.typing import NDArray3
from pymesh.utils import (
    validate_move_parameters,
    validate_rotate_parameters,
    validate_surface_path_parameters,
)


class RuledSurface(Surface):
    """Creates a ruled surface based on two curves
    and creates mesh points for generating panels.
    """

    curve1 = AsInstanceOf(Curve)
    curve2 = AsInstanceOf(Curve)

    def __init__(self, curve1: Curve, curve2: Curve):
        self._all_surfaces.append(self)
        self.curve1 = curve1
        self.curve2 = curve2
        super().__init__()

    def __eq__(self, other):
        return self.curve1 == other.curve1 and self.curve2 == other.curve2

    def __repr__(self):
        return f"{type(self).__name__}(curve1={self.curve1!r}, curve2={self.curve2!r})"

    def get_max_lengths(self) -> tuple[float]:
        length_u = max(self.curve1.length, self.curve2.length)
        length_w = max(
            float(np.sqrt(np.sum((self.curve1.start - self.curve2.start) ** 2))),
            float(np.sqrt(np.sum((self.curve1.end - self.curve2.end) ** 2))),
        )
        return length_u, length_w

    def path(
        self, u: int | float, w: int | float, uflip: bool = False, wflip: bool = False
    ) -> NDArray3[np.float64]:
        u, w = validate_surface_path_parameters(u, w, uflip, wflip)
        return (1 - w) * self.curve1.path(u) + w * self.curve2.path(u)

    def copy(self) -> Self:
        return RuledSurface(self.curve1.copy(), self.curve2.copy())

    def move(
        self, dx: int | float = 0.0, dy: int | float = 0.0, dz: int | float = 0.0
    ) -> Self:
        validate_move_parameters(dx, dy, dz)
        self.curve1.move(dx, dy, dz)
        self.curve2.move(dx, dy, dz)
        return self

    def rotate(self, axis: Vector3D, angle: int | float) -> Self:
        validate_rotate_parameters(axis, angle)
        self.curve1.rotate(axis, angle)
        self.curve2.rotate(axis, angle)
        return self

    def mirror(
        self,
        a: int | float,
        b: int | float,
        c: int | float,
        x0: int | float = 0.0,
        y0: int | float = 0.0,
        z0: int | float = 0.0,
    ) -> Self:
        self.curve1.mirror(a, b, c, x0, y0, z0)
        self.curve2.mirror(a, b, c, x0, y0, z0)
        return self
