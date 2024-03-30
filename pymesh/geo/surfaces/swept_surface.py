"""Module including the SweptSurface class
"""

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


class SweptSurface(Surface):
    """Creates a surface based on a curve swept by another
    and creates mesh points for generating panels.
    """

    curve = AsInstanceOf(Curve)
    sweeper = AsInstanceOf(Curve)

    def __init__(self, curve: Curve, sweeper: Curve):
        """Creates a swept surface using a curve and a sweeper curve.

        curve: defines the path to be swept

        sweper: defines the path curve is swept along
        """
        self._all_surfaces.append(self)
        self.curve = curve
        self.sweeper = sweeper
        super().__init__()

    def __eq__(self, other):
        return self.curve == other.curve and self.sweeper == other.sweeper

    def __repr__(self):
        return f"{type(self).__name__}(curve={self.curve!r}, sweeper={self.sweeper!r})"

    def get_max_lengths(self) -> tuple[float]:
        return self.curve.length, self.sweeper.length

    def path(
        self, u: int | float, w: int | float, uflip: bool = False, wflip: bool = False
    ) -> NDArray3[np.float64]:
        u, w = validate_surface_path_parameters(u, w, uflip, wflip)
        sweep = self.sweeper.path(w) - self.sweeper.path(0)
        return self.curve.path(u) + sweep

    def copy(self) -> Self:
        return SweptSurface(self.curve.copy(), self.sweeper.copy())

    def move(
        self, dx: int | float = 0.0, dy: int | float = 0.0, dz: int | float = 0.0
    ) -> Self:
        validate_move_parameters(dx, dy, dz)
        self.curve.move(dx, dy, dz)
        self.sweeper.move(dx, dy, dz)
        return self

    def rotate(
        self,
        angle: int | float,
        a: int | float,
        b: int | float,
        c: int | float,
        x0: int | float = 0.0,
        y0: int | float = 0.0,
        z0: int | float = 0.0,
    ) -> Self:
        self.curve.rotate(angle, a, b, c, x0, y0, z0)
        self.sweeper.rotate(angle, a, b, c, x0, y0, z0)
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
        self.curve.mirror(a, b, c, x0, y0, z0)
        self.sweeper.mirror(a, b, c, x0, y0, z0)
        return self
