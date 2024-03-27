"""Module including the ruled surface class
"""

import numpy as np

from pymesh.geo.curves.curve import Curve
from pymesh.typing import NDArray3
from pymesh.mesh.surface_mesh_generator import SurfaceMeshGenerator
from pymesh.geo.surfaces.surface import Surface, validate_surface_path_parameters


class RuledSurface(Surface):
    """Creates a ruled surface based on two curves
    and creates mesh points for generating panels.
    """

    def __init__(self, curve_1: Curve, curve_2: Curve):
        self._all_surfaces.append(self)
        self.curve_1 = curve_1
        self.curve_2 = curve_2
        self._set_mesh_generator(
            SurfaceMeshGenerator(self.get_path(), self.get_max_lengths()), force=True
        )

    @property
    def curve_1(self) -> Curve:
        return self._curve_1

    @curve_1.setter
    def curve_1(self, value) -> None:
        if not isinstance(value, Curve):
            raise TypeError("curve_1 must be of type 'Curve'")
        self._curve_1 = value

    @property
    def curve_2(self) -> Curve:
        return self._curve_2

    @curve_2.setter
    def curve_2(self, value) -> None:
        if not isinstance(value, Curve):
            raise TypeError("curve_2 must be of type 'Curve'")
        self._curve_2 = value

    def get_max_lengths(self) -> tuple[float]:
        """Returns longest boundary length along the u and w dimensions.

        u: largest distance along curve paths.
        w: largest distance between opposing curves end points.
        """
        start_points = [self.curve_1.start, self.curve_2.start]
        end_points = [self.curve_1.end, self.curve_2.end]
        length_u = max(self.curve_1.length, self.curve_2.length)
        length_w = max(
            float(np.sqrt(np.sum((start_points[0] - start_points[1]) ** 2))),
            float(np.sqrt(np.sum((end_points[0] - end_points[1]) ** 2))),
        )
        return length_u, length_w

    def path(
        self, u: int | float, w: int | float, uflip: bool = False, wflip: bool = False
    ) -> NDArray3[np.float64]:
        u, w = validate_surface_path_parameters(u, w, uflip, wflip)
        return (1 - w) * self.curve_1.path(u) + w * self.curve_2.path(u)
