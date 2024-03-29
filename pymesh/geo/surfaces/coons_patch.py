"""Module including the coons patch class
"""

from typing import Self

import numpy as np

from pymesh.exceptions import CurveIntersectionError
from pymesh.geo.curves.curve import Curve
from pymesh.geo.surfaces.surface import Surface
from pymesh.mesh.mesh_generator import MeshGenerator
from pymesh.typing import NDArray3
from pymesh.utils import validate_move_parameters, validate_surface_path_parameters

# ! Consider using sets instead of list|tuple: enforcing uniquenes !


class CoonsPatch(Surface):
    """Coons patch class taking a selection of four curves
    and creates mesh points for generating panels.
    """

    def __init__(self, curves: list[Curve] | tuple[Curve]):
        self._all_surfaces.append(self)
        self.curves = curves  # also sets self._flipped_curves
        super().__init__()

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
        ref_point = curve_selection[-1].end
        flipped_curves = [False]
        index = 0
        while (
            len(curve_selection) <= 4
            and len(initial_selection) >= 1
            and index < len(initial_selection)
        ):
            next_curve_points = (
                initial_selection[index].start,
                initial_selection[index].end,
            )
            print(ref_point, next_curve_points)
            if ref_point == next_curve_points[0] or ref_point == next_curve_points[1]:
                if np.all(ref_point == next_curve_points[0]):
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
        if ref_point != curve_selection[0].start or index > len(initial_selection):
            raise CurveIntersectionError(
                "Selected curves does not share intersection points"
            )
        cflip, cselect = self._set__curve_order(flipped_curves, curve_selection)
        self._flipped_curves = tuple(cflip)
        self._curves = tuple(cselect)

    # @curves.setter
    # def curves(self, curves) -> None:
    #     pname = "curves"
    #     if not isinstance(curves, (list, tuple)):
    #         raise TypeError(f"{pname} must receive a list or tuple input")
    #     if len(curves) != 4:
    #         raise ValueError(f"{pname} must containing exactly 4 items.")
    #     for curve in curves:
    #         if not isinstance(curve, Curve):
    #             raise TypeError(f"{pname} items must be of type 'Curve'.")
    #     initial_selection = list(curves)
    #     curve_selection = [initial_selection.pop(0)]
    #     ref_point = curve_selection[-1].end
    #     flipped_curves = [False]
    #     index = 0
    #     while (
    #         len(curve_selection) <= 4
    #         and len(initial_selection) >= 1
    #         and index < len(initial_selection)
    #     ):
    #         next_curve_points = (
    #             initial_selection[index].start,
    #             initial_selection[index].end,
    #         )
    #         print(ref_point, next_curve_points)
    #         if np.all(ref_point == next_curve_points[0]) or np.all(
    #             ref_point == next_curve_points[1]
    #         ):
    #             if np.all(ref_point == next_curve_points[0]):
    #                 # next curve has matching starting point
    #                 flipped_curves.append(False)
    #                 ref_point = next_curve_points[1]
    #             else:
    #                 # next curve has matching ending point
    #                 flipped_curves.append(True)
    #                 ref_point = next_curve_points[0]
    #             curve_selection.append(initial_selection.pop(index))
    #             index = 0
    #             continue
    #         index += 1
    #     if np.any(ref_point != curve_selection[0].start) or index > len(
    #         initial_selection
    #     ):
    #         raise CurveIntersectionError(
    #             "Selected curves does not share intersection points"
    #         )
    #     cflip, cselect = self._set__curve_order(flipped_curves, curve_selection)
    #     self._flipped_curves = tuple(cflip)
    #     self._curves = tuple(cselect)

    @staticmethod
    def _set__curve_order(cflip, cselect) -> tuple[list]:
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

        def path_u0(x):
            return curve_u0.path(x, flip=fu0)

        def path_u1(x):
            return curve_u1.path(x, flip=fu1)

        def path_0w(x):
            return curve_0w.path(x, flip=f0w)

        def path_1w(x):
            return curve_1w.path(x, flip=f1w)

        p00, p11, p01, p10 = path_u0(0), path_u1(1), path_0w(1), path_1w(0)
        p1 = (1 - u) * path_0w(w) + u * path_1w(w)
        p2 = (1 - w) * path_u0(u) + w * path_u1(u)
        p3 = (
            (1 - u) * (1 - w) * p00
            + u * (1 - w) * p10
            + (1 - u) * w * p01
            + u * w * p11
        )
        return p1 + p2 - p3

    def get_max_lengths(self) -> tuple[float]:
        curve_u0, curve_u1, curve_0w, curve_1w = self.curves
        max_length_u = max(curve_u0.length, curve_u1.length)
        max_length_w = max(curve_0w.length, curve_1w.length)
        return max_length_u, max_length_w

    def copy(self) -> Self:
        curve_u0, curve_u1, curve_0w, curve_1w = self.curves
        new_curves = (
            curve_u0.copy(),
            curve_u1.copy(),
            curve_0w.copy(),
            curve_1w.copy(),
        )
        return CoonsPatch(new_curves)

    def move(
        self, dx: int | float = 0.0, dy: int | float = 0.0, dz: int | float = 0.0
    ) -> None:
        validate_move_parameters(dx, dy, dz)
        for curve in self.curves:
            curve.move(dx, dy, dz)
