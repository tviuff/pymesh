"""Module including the coons patch class
"""

import numpy as np

from pymesh.geo.curves.curve import Curve
from pymesh.utils.typing import NDArray3, NDArray3xNxN
from pymesh.utils.exceptions import CurveIntersectionError
from pymesh.mesh.surface_mesh_generator import SurfaceMeshGenerator
from pymesh.geo.surfaces.surface import Surface, validate_surface_path_parameters

# ! Consider using sets instead of list|tuple: enforcing uniquenes !


class CoonsPatch(Surface):
    """Coons patch class taking a selection of four curves
    and creates mesh points for generating panels.
    """

    def __init__(self, curves: list[Curve] | tuple[Curve]):
        self._all_surfaces.append(self)
        self.curves = curves  # also sets self._flipped_curves
        self._set_mesh_generator(
            SurfaceMeshGenerator(self.get_path(), self.get_max_lengths()), force=True
        )

    @property
    def curves(self) -> tuple[Curve]:
        return self._curves

    @curves.setter
    def curves(self, curves) -> None:
        pname = "curves"
        if not isinstance(curves, (list, tuple)):
            raise TypeError(f"{pname} must receive a list or tuple input")
        if len(curves) != 4:
            raise ValueError(f"{pname} must containing exactly 4 items.")
        for curve in curves:
            if not isinstance(curve, Curve):
                raise TypeError(f"{pname} items must be of type 'Curve'.")
        initial_selection = list(curves)
        curve_selection = [initial_selection.pop(0)]
        ref_point = curve_selection[-1].point_end
        flipped_curves = [False]
        index = 0
        while (
            len(curve_selection) <= 4
            and len(initial_selection) >= 1
            and index < len(initial_selection)
        ):
            next_curve_points = (
                initial_selection[index].point_start,
                initial_selection[index].point_end,
            )
            if ref_point in next_curve_points:
                if ref_point == next_curve_points[0]:
                    # next curve has matching starting point
                    flipped_curves.append(False)
                    ref_point = next_curve_points[1]
                else:
                    # next curve has matching ending point
                    flipped_curves.append(True)
                    ref_point = next_curve_points[0]
                curve_selection.append(initial_selection.pop(index))
                index = 0
                continue
            index += 1
        if ref_point != curve_selection[0].point_start or index > len(
            initial_selection
        ):
            raise CurveIntersectionError(
                "Selected curves does not share intersection points"
            )
        cflip, cselect = self._set_coons_patch_curve_order(
            flipped_curves, curve_selection
        )
        self._flipped_curves = tuple(cflip)
        self._curves = tuple(cselect)

    @staticmethod
    def _set_coons_patch_curve_order(cflip, cselect) -> tuple[list]:
        """Sets the order u0, u1, 0w, 1w where u0 = first item in cselect"""
        cselect = [cselect[0], cselect[2], cselect[3], cselect[1]]
        cflip = [cflip[0], cflip[2], cflip[3], cflip[1]]
        for index in (1, 2):
            cflip[index] = not cflip[index]
        return cflip, cselect

    def path(
        self, u: int | float, w: int | float, uflip: bool = False, wflip: bool = False
    ) -> NDArray3[np.float64]:
        u, w = validate_surface_path_parameters(u, w, uflip, wflip)
        curve_u0, curve_u1, curve_0w, curve_1w = self.curves
        fu0, fu1, f0w, f1w = self._flipped_curves

        def cu0(x):
            func = curve_u0.get_path()
            return func(x, flip=fu0)

        def cu1(x):
            func = curve_u1.get_path()
            return func(x, flip=fu1)

        def c0w(x):
            func = curve_0w.get_path()
            return func(x, flip=f0w)

        def c1w(x):
            func = curve_1w.get_path()
            return func(x, flip=f1w)

        p00, p11, p01, p10 = cu0(0), cu1(1), c0w(1), c1w(0)
        p1 = (1 - u) * c0w(w) + u * c1w(w)
        p2 = (1 - w) * cu0(u) + w * cu1(u)
        p3 = (
            (1 - u) * (1 - w) * p00
            + u * (1 - w) * p10
            + (1 - u) * w * p01
            + u * w * p11
        )
        p = p1 + p2 - p3
        return p

    def get_max_lengths(self) -> tuple[float]:
        curve_u0, curve_u1, curve_0w, curve_1w = self.curves
        max_length_u = max(curve_u0.length, curve_u1.length)
        max_length_w = max(curve_0w.length, curve_1w.length)
        return max_length_u, max_length_w

    @property
    def mesh_points(self) -> NDArray3xNxN[np.float64]:
        return self.mesher.generate_mesh_points()
