"""Module including the swept surface class
"""

import numpy as np

from pymesh.geo.curves.curve import Curve
from pymesh.mesh.surface_mesh_generator import SurfaceMeshGenerator
from pymesh.typing import NDArray3
from pymesh.geo.surfaces.surface import Surface, validate_surface_path_parameters


class SweptSurface(Surface):
    """Creates a surface based on a curve swept by another
    and creates mesh points for generating panels.
    """

    def __init__(self, curve: Curve, sweeper_curve: Curve):
        self._all_surfaces.append(self)
        self.curve = curve
        self.sweeper_curve = sweeper_curve
        self._set_mesh_generator(
            SurfaceMeshGenerator(self.get_path(), self.get_max_lengths()), force=True
        )

    @property
    def curve(self) -> Curve:
        return self._curve

    @curve.setter
    def curve(self, curve: Curve) -> None:
        if not isinstance(curve, Curve):
            raise TypeError("curve must be of type 'Curve'")
        self._curve = curve

    @property
    def sweeper_curve(self) -> Curve:
        return self._sweeper_curve

    @sweeper_curve.setter
    def sweeper_curve(self, value: Curve) -> None:
        if not isinstance(value, Curve):
            raise TypeError("sweeper_curve must be of type 'Curve'")
        self._sweeper_curve = value

    def path(
        self, u: int | float, w: int | float, uflip: bool = False, wflip: bool = False
    ) -> NDArray3[np.float64]:
        u, w = validate_surface_path_parameters(u, w, uflip, wflip)
        return self.curve.path(u) + self.sweeper_curve.path(w)

    def get_max_lengths(self) -> tuple[float]:
        return self.curve.length, self.sweeper_curve.length
