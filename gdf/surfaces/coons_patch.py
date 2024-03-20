"""Module including the coons patch class
"""

import numpy as np
from numpy import ndarray

from gdf.surfaces import Surface
from gdf.curves import Curve
from gdf.mesh.descriptors import BoundaryDistribution, MeshNumber
from gdf.constants import MeshConstants
from gdf.exceptions import CurveIntersectionError

class CoonsPatch(Surface):
    """Coons patch class taking a selection of four curves
    and creates mesh points for generating panels.
    """

    dist_u0 = BoundaryDistribution()
    dist_u1 = BoundaryDistribution()
    dist_0w = BoundaryDistribution()
    dist_1w = BoundaryDistribution()
    num_points_u = MeshNumber()
    num_points_w = MeshNumber()

    def __init__(self, curve_u0:Curve, curve_u1:Curve, curve_0w:Curve, curve_1w:Curve):
        self._all_surfaces.append(self)
        self.curve_selection = (curve_u0, curve_u1, curve_0w, curve_1w)
        self.dist_u0 = MeshConstants.DEFAULT_DIST_METHOD.value
        self.dist_u1 = MeshConstants.DEFAULT_DIST_METHOD.value
        self.dist_0w = MeshConstants.DEFAULT_DIST_METHOD.value
        self.dist_1w = MeshConstants.DEFAULT_DIST_METHOD.value
        self.num_points_u = MeshConstants.DEFAULT_NUM_POINT.value
        self.num_points_w = MeshConstants.DEFAULT_NUM_POINT.value

    @property
    def curve_selection(self)-> tuple[Curve]:
        return self._curve_selection

    @curve_selection.setter
    def curve_selection(self, curves) -> None:
        pname = "curve_selection"
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
        while len(curve_selection) <= 4 and len(initial_selection) >= 1 and index <= 2:
            next_curve_points = (
                initial_selection[index].point_start,
                initial_selection[index].point_end
            )
            if ref_point in next_curve_points:
                if ref_point == next_curve_points[0]:
                    flipped_curves.append(False)
                    ref_point = next_curve_points[1]
                else:
                    # flip direction of curve to match points
                    flipped_curves.append(True)
                    ref_point = next_curve_points[0]
                curve_selection.append(initial_selection.pop(index))
                index = 0
                continue
            index += 1
        if ref_point != curve_selection[0].point_start or index > 2:
            raise CurveIntersectionError("Selected curves does not share intersection points")
        cflip, cselect = self._set_coons_patch_curve_order(flipped_curves, curve_selection)
        self._curve_selection = tuple(cselect)
        self._flipped_curves = tuple(cflip)

    @property
    def flipped_curves(self) -> tuple[bool]:
        return self._flipped_curves

    def _set_coons_patch_curve_order(self, cflip, cselect) -> tuple[list]:
        """Sets the order u0, u1, 0w, 1w where u0 = first item in cselect"""
        cselect = [cselect[0], cselect[2], cselect[3], cselect[1]]
        cflip = [cflip[0], cflip[2], cflip[3], cflip[1]]
        for index in (1, 2):
            cflip[index] = not cflip[index]
        return cflip, cselect

    @property
    def mesh_points(self) -> ndarray:
        npu = self.num_points_u
        npw = self.num_points_w
        flipu0 = self.flipped_curves[0]
        flipu1 = self.flipped_curves[1]
        flip0w = self.flipped_curves[2]
        flip1w = self.flipped_curves[3]
        du0 = self.dist_u0.get_fn(flip_dir=flipu0)
        du1 = self.dist_u1.get_fn(flip_dir=flipu1)
        d0w = self.dist_0w.get_fn(flip_dir=flip0w)
        d1w = self.dist_1w.get_fn(flip_dir=flip1w)
        pu0 = self.curve_selection[0].get_path_fn()
        pu1 = self.curve_selection[1].get_path_fn()
        p0w = self.curve_selection[2].get_path_fn()
        p1w = self.curve_selection[3].get_path_fn()
        p00 = pu0(du0(0))
        p11 = pu1(du1(1))
        p01 = p0w(d0w(1))
        p10 = p1w(d1w(0))
        mp = np.zeros((3, npu, npw))
        for i, u in enumerate(np.linspace(0, 1, num=npu, endpoint=True)):
            for j, w in enumerate(np.linspace(0, 1, num=npw, endpoint=True)):
                p1 = (1-u)*p0w(d0w(w)) + u*p1w(d1w(w))
                p2 = (1-w)*pu0(du0(u)) + w*pu1(du1(u))
                p3 = (1-u)*(1-w)*p00 + u*(1-w)*p10 + (1-u)*w*p01 + u*w*p11
                mp[:, i, j] = p1 + p2 - p3
        return mp
