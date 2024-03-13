"""Module including the coons patch class
"""

import numpy as np
from numpy import ndarray

from gdfgen.surfaces import Surface
from gdfgen.curves import Curve
from gdfgen.mesh import DistMethod, BoundaryDistribution, MeshNumber
from gdfgen.constants import MeshConstants as MConst
from gdfgen.exceptions import CurveIntersectionError

# ! ERROR if num_points_u != num_points_w

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
        self.curve_selection = (curve_u0, curve_u1, curve_0w, curve_1w)
        self.dist_u0 = MConst.DEFAULT_DIST_METHOD.value
        self.dist_u1 = MConst.DEFAULT_DIST_METHOD.value
        self.dist_0w = MConst.DEFAULT_DIST_METHOD.value
        self.dist_1w = MConst.DEFAULT_DIST_METHOD.value
        self.num_points_u = MConst.DEFAULT_NUM_POINT.value
        self.num_points_w = MConst.DEFAULT_NUM_POINT.value

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
        cselect = [cselect[0], cselect[2], cselect[3], cselect[1]]
        cflip = [cflip[0], cflip[2], cflip[3], cflip[1]]
        for index in (1, 2):
            cflip[index] = not cflip[index]
        return cflip, cselect

    def _get_dist_methods(self) -> tuple[DistMethod]:
        """Returns curve path point distribution methods."""
        return self.dist_u0, self.dist_u1, self.dist_0w, self.dist_1w

    def _get_curve_path_points(self) -> tuple[ndarray]:
        """Returns path points for each of the four input curves."""
        curve_paths = []
        num_points = tuple(2*[self.num_points_u, self.num_points_w])
        flipped_curves = self.flipped_curves
        dists = self._get_dist_methods()
        for curve, num, dist, flip in zip(self.curve_selection, num_points, dists, flipped_curves):
            path_xyz = curve.get_path_xyz(num_points=num, dist_method=dist, flip_dir=flip)
            curve_paths.append(path_xyz)
        pu0, pu1, p0w, p1w = tuple(curve_paths)
        return pu0, pu1, p0w, p1w

    @property
    def mesh_points(self) -> ndarray:
        pu0, pu1, p0w, p1w = self._get_curve_path_points()
        p00 = pu0[ 0, :]
        p11 = pu1[-1, :]
        p01 = p0w[-1, :]
        p10 = p1w[ 0, :]
        mp = np.zeros((3, self.num_points_u, self.num_points_w))
        for i, u in enumerate(np.linspace(0, 1, num=self.num_points_u, endpoint=True)):
            for j, w in enumerate(np.linspace(0, 1, num=self.num_points_w, endpoint=True)):
                p1 = (1-u)*p0w[j,:] + u*p1w[j,:]
                p2 = (1-w)*pu0[i,:] + w*pu1[i,:]
                p3 = (1-u)*(1-w)*p00 + u*(1-w)*p10 + (1-u)*w*p01 + u*w*p11
                for k in range(0, 3):
                    mp[k,i,j] = p1[k] + p2[k] - p3[k]
        return mp
