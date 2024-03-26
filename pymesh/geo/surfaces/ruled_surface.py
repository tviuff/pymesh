"""Module including the ruled surface class
"""

import numpy as np

from pymesh.geo.curves.curve import Curve
from pymesh.utils.typing import NDArray3, NDArray3xNxN
from pymesh.mesh.surface_mesh_generator import SurfaceMeshGenerator
from pymesh.geo.surfaces.surface import Surface, validate_path_parameters


class RuledSurface(Surface):
    """Creates a ruled surface based on two curves
    and creates mesh points for generating panels.
    """

    def __init__(self, curve_1: Curve, curve_2: Curve):
        self._all_surfaces.append(self)
        self.curve_1 = curve_1
        self.curve_2 = curve_2
        self.mesher = SurfaceMeshGenerator(self.get_path(), self.get_max_lengths())

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

        1) largest distance along curve paths.
        2) largest distance between opposing curves end points.
        """
        length_1 = max(self.curve_1.length, self.curve_2.length)
        start_points = (self.curve_1.point_start.xyz, self.curve_2.point_start.xyz)
        end_points = (self.curve_1.point_end.xyz, self.curve_2.point_end.xyz)
        length_2_start = float(
            np.sqrt(np.sum((start_points[0] - start_points[1]) ** 2))
        )
        length_2_end = float(np.sqrt(np.sum((end_points[0] - end_points[1]) ** 2)))
        length_2 = max(length_2_start, length_2_end)
        return length_1, length_2

    def path(self, u: int | float, w: int | float) -> NDArray3[np.float64]:
        u, w = validate_path_parameters(u, w)
        return (1 - w) * self.curve_1.path(u) + w * self.curve_2.path(u)

    @property
    def mesh_points(self) -> NDArray3xNxN[np.float64]:
        return self.mesher.generate_mesh_points()
