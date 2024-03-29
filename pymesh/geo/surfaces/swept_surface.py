"""Module including the SweptSurface class
"""

from typing import Self

import numpy as np

from pymesh.descriptors import AsInstanceOf
from pymesh.geo.curves.curve import Curve
from pymesh.geo.surfaces.surface import Surface
from pymesh.typing import NDArray3
from pymesh.utils import validate_move_parameters, validate_surface_path_parameters


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

    def get_max_lengths(self) -> tuple[float]:
        return self.curve.length, self.sweeper.length

    def path(
        self, u: int | float, w: int | float, uflip: bool = False, wflip: bool = False
    ) -> NDArray3[np.float64]:
        u, w = validate_surface_path_parameters(u, w, uflip, wflip)
        return self.curve.path(u) + self.sweeper.path(w)

    def copy(self) -> Self:
        return SweptSurface(self.curve.copy(), self.sweeper.copy())

    def move(
        self, dx: int | float = 0.0, dy: int | float = 0.0, dz: int | float = 0.0
    ) -> None:
        validate_move_parameters(dx, dy, dz)
        self.curve.move(dx, dy, dz)
        self.sweeper.move(dx, dy, dz)
