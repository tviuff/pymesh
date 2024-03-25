"""Module including the coons patch class
"""

import numpy as np

from pygdf.curves.curve import Curve
from pygdf.constants import MeshConstants
from pygdf.custom_types import NDArray3, NDArray3xNxN
from pygdf.descriptors import AsNumber, AsInstanceOf
from pygdf.exceptions import CurveIntersectionError
from pygdf.mesh.distributions import MeshDistribution
from pygdf.surfaces.surface import Surface, validate_path_parameters

# ! Consider using sets instead of list|tuple: enforcing uniquenes !


class CoonsPatch(Surface):
    """Coons patch class taking a selection of four curves
    and creates mesh points for generating panels.
    """

    boundary_distribution_u = AsInstanceOf(MeshDistribution)
    boundary_distribution_w = AsInstanceOf(MeshDistribution)
    panel_density_u = AsNumber(minvalue=0)
    panel_density_w = AsNumber(minvalue=0)

    def __init__(self, curves: list[Curve] | tuple[Curve]):
        self._all_surfaces.append(self)
        self.boundary_distribution_u = MeshConstants.DEFAULT_DISTRIBUTION_METHOD.value()
        self.boundary_distribution_w = MeshConstants.DEFAULT_DISTRIBUTION_METHOD.value()
        self.panel_density_u = MeshConstants.DEFAULT_DENSITY.value
        self.panel_density_w = MeshConstants.DEFAULT_DENSITY.value
        self.curves = curves  # also sets self._flipped_curves

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

    def _get_num_points(self) -> tuple[int]:
        density_u, density_w = self.panel_density_u, self.panel_density_w
        num_points_u, num_points_w = density_u + 1, density_w + 1
        if isinstance(density_u, float) or isinstance(density_w, float):
            curve_u0, curve_u1, curve_0w, curve_1w = self.curves
            if isinstance(density_u, float):
                u_length = max(curve_u0.length, curve_u1.length)
                num_points_u = int(np.ceil(u_length / density_u) + 1)
            if isinstance(density_w, float):
                w_length = max(curve_0w.length, curve_1w.length)
                num_points_w = int(np.ceil(w_length / density_w) + 1)
        return num_points_u, num_points_w

    def path(self, u: int | float, w: int | float) -> NDArray3[np.float64]:
        u, w = validate_path_parameters(u, w)
        flip = [-1 if flipped else 1 for flipped in self._flipped_curves]
        p00 = self.curves[0].path(flip[0] * 0)
        p11 = self.curves[1].path(flip[1] * 1)
        p01 = self.curves[2].path(flip[2] * 1)
        p10 = self.curves[3].path(flip[3] * 0)
        p1 = (1 - u) * w + u * w
        p2 = (1 - w) * u + w * u
        p3 = (
            (1 - u) * (1 - w) * p00
            + u * (1 - w) * p10
            + (1 - u) * w * p01
            + u * w * p11
        )
        return p1 + p2 - p3

    @property
    def mesh_points(self) -> NDArray3xNxN[np.float64]:
        npu, npw = self._get_num_points()
        du1 = self.boundary_distribution_u.get_dist_fn()
        d0w = self.boundary_distribution_w.get_dist_fn()
        du0 = self.boundary_distribution_u.get_dist_fn()
        d1w = self.boundary_distribution_w.get_dist_fn()
        path_fns = []
        for curve, flip in zip(self.curves, self._flipped_curves):
            path_fns.append(curve.get_path_fn(flip_direction=flip))
        pu0, pu1, p0w, p1w = path_fns
        p00 = pu0(du0(0))
        p11 = pu1(du1(1))
        p01 = p0w(d0w(1))
        p10 = p1w(d1w(0))
        mp = np.zeros((3, npu, npw))
        for i, u in enumerate(np.linspace(0, 1, num=npu, endpoint=True)):
            for j, w in enumerate(np.linspace(0, 1, num=npw, endpoint=True)):
                p1 = (1 - u) * p0w(d0w(w)) + u * p1w(d1w(w))
                p2 = (1 - w) * pu0(du0(u)) + w * pu1(du1(u))
                p3 = (
                    (1 - u) * (1 - w) * p00
                    + u * (1 - w) * p10
                    + (1 - u) * w * p01
                    + u * w * p11
                )
                mp[:, i, j] = p1 + p2 - p3
        return mp
