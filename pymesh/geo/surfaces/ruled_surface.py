"""Module containing the ruled RuledSurface class"""

from typing import Self

import numpy as np

from pymesh.descriptors import AsInstanceOf
from pymesh.geo.curves.curve import Curve
from pymesh.geo.surfaces.surface import Surface
from pymesh.typing import NDArray3
from pymesh.utils import validate_move_parameters, validate_surface_path_parameters


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
    ) -> None:
        validate_move_parameters(dx, dy, dz)
        self.curve1.move(dx, dy, dz)
        self.curve2.move(dx, dy, dz)
