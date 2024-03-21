"""Module including the coons patch class
"""

import numpy as np
from numpy import ndarray

from gdf.surfaces import Surface
from gdf.curves import Curve
from gdf.mesh.descriptors import BoundaryDistribution, MeshNumber
from gdf.mesh.distribution_methods import DistributionMethod
from gdf.constants import MeshConstants
from gdf.exceptions import CurveIntersectionError

# ! cleanup: .curves .dist_u .dist_w
# ! .dists (shape = 4) instead of flipped_curves and apply flipping directly

class CoonsPatch(Surface):
    """Coons patch class taking a selection of four curves
    and creates mesh points for generating panels.
    """

    dist_u = BoundaryDistribution()
    dist_w = BoundaryDistribution()
    num_points_u = MeshNumber()
    num_points_w = MeshNumber()

    def __init__(self, curves:list[Curve]|tuple[Curve]):
        self._all_surfaces.append(self)
        self.dist_u = MeshConstants.DEFAULT_DIST_METHOD.value()
        self.dist_w = MeshConstants.DEFAULT_DIST_METHOD.value()
        self.num_points_u = MeshConstants.DEFAULT_NUM_POINT.value
        self.num_points_w = MeshConstants.DEFAULT_NUM_POINT.value
        self.curves = curves # also sets flipped_curves

    @property
    def distribution_methods(self)-> tuple[DistributionMethod]:
        return tuple([self.dist_u, self.dist_u, self.dist_w, self.dist_w])

    @property
    def flipped_curves(self) -> tuple[bool]:
        return self._flipped_curves

    @property
    def curves(self)-> tuple[Curve]:
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
        self._flipped_curves = tuple(cflip)
        self._curves = tuple(cselect)

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
        du0 = self.distribution_methods[0].get_dist_fn()
        du1 = self.distribution_methods[1].get_dist_fn()
        d0w = self.distribution_methods[2].get_dist_fn()
        d1w = self.distribution_methods[3].get_dist_fn()
        path_fns = []
        for curve, flip in zip(self.curves, self.flipped_curves):
            path_fns.append(curve.get_path_fn(flip_direction=flip))
        pu0 = path_fns[0]
        pu1 = path_fns[1]
        p0w = path_fns[2]
        p1w = path_fns[3]
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
