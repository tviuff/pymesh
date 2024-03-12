"""Module including the coons patch class
"""

import numpy as np

from gdfgen.surfaces import Surface
from gdfgen.curves import Curve
from gdfgen.mesh import DistMethod
from gdfgen.constants import MeshConstants as MConst
from gdfgen.exceptions import CurveIntersectionError

class CoonsPatch(Surface):
    """Coons patch class taking a selection of four curves
    and creates mesh points for generating panels.
    """

    curve_selection:tuple[Curve] = None
    flipped_curves:tuple[bool] = None
    _dist_u0:DistMethod = MConst.DEFAULT_DIST_METHOD.value
    _dist_u1:DistMethod = MConst.DEFAULT_DIST_METHOD.value
    _dist_0w:DistMethod = MConst.DEFAULT_DIST_METHOD.value
    _dist_1w:DistMethod = MConst.DEFAULT_DIST_METHOD.value
    _num_points_u:int = MConst.DEFAULT_NUM_POINT.value
    _num_points_w:int = MConst.DEFAULT_NUM_POINT.value

    def __init__(self, curve_u0:Curve, curve_u1:Curve, curve_0w:Curve, curve_1w:Curve):
        """Initializing Coons Patch curves."""
        self.__validate_selection_of_curve_types(curve_u0, curve_u1, curve_0w, curve_1w)
        self.__validate_closed_curve_and_set_curve_selection(curve_u0, curve_u1, curve_0w, curve_1w)

    def __validate_selection_of_curve_types(self, curve_u0, curve_u1, curve_0w, curve_1w) -> None:
        """Validates selection with type 'Curve' items."""
        curve_selection = curve_u0, curve_u1, curve_0w, curve_1w
        for curve in curve_selection:
            if not isinstance(curve, Curve):
                raise TypeError("Curve input must be of type 'Curve'.")

    def __validate_closed_curve_and_set_curve_selection(self,
            curve_u0, curve_u1, curve_0w, curve_1w
            ) -> None:
        """Validates selection with shared intersection points.
        Enforces the direction of the first curve in the original curve sellection."""
        initial_selection = [curve_u0, curve_u1, curve_0w, curve_1w]
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
                    # Flip direction of curve to match points
                    flipped_curves.append(True)
                    ref_point = next_curve_points[0]
                curve_selection.append(initial_selection.pop(index))
                index = 0
                continue
            index += 1
        if ref_point != curve_selection[0].point_start or index > 2:
            raise CurveIntersectionError("Selected curves does not share intersection points")
        cflip, cselect = self.__set_coons_patch_curve_order(flipped_curves, curve_selection)
        self.flipped_curves = tuple(cflip)
        self.curve_selection = tuple(cselect)

    def __set_coons_patch_curve_order(self, cflip, cselect) -> tuple[list]:
        cselect = [cselect[0], cselect[2], cselect[3], cselect[1]]
        cflip = [cflip[0], cflip[2], cflip[3], cflip[1]]
        for index in (1, 2):
            cflip[index] = not cflip[index]
        return cflip, cselect

    def set_dist_methods(self,
            dist_u0:DistMethod = MConst.DEFAULT_DIST_METHOD.value,
            dist_u1:DistMethod = MConst.DEFAULT_DIST_METHOD.value,
            dist_0w:DistMethod = MConst.DEFAULT_DIST_METHOD.value,
            dist_1w:DistMethod = MConst.DEFAULT_DIST_METHOD.value,
        ):
        """Specifies curve path distribution methods, default is 'linear'."""
        self._dist_u0 = dist_u0
        self._dist_u1 = dist_u1
        self._dist_0w = dist_0w
        self._dist_1w = dist_1w

    def _get_dist_methods(self):
        """Returns curve path point distribution methods."""
        return self._dist_u0, self._dist_u1, self._dist_0w, self._dist_1w

    def get_num_points(self):
        """Returns number of points along u and w dimensions."""
        return self._num_points_u, self._num_points_w

    def set_num_points(self,
            num_points_u:int = MConst.DEFAULT_NUM_POINT.value,
            num_points_w:int = MConst.DEFAULT_NUM_POINT.value
        ):
        """Specify number of points along normalized u and w dimensions."""
        if not isinstance(num_points_u, int):
            raise TypeError("num_points_u must be of type 'int'")
        if not isinstance(num_points_w, int):
            raise TypeError("num_points_w must be of type 'int'")
        self._num_points_u = num_points_u
        self._num_points_w = num_points_w

    def _get_curve_path_points(self):
        """Returns path points for each of the four input curves."""
        curve_paths = []
        num_points_u, num_points_w = self.get_num_points()
        num_points = (num_points_u, num_points_u, num_points_w, num_points_w)
        flipped_curves = self.flipped_curves
        dists = self._get_dist_methods()
        for curve, num, dist, flip in zip(self.curve_selection, num_points, dists, flipped_curves):
            path_fn = curve.get_path_fn(num_points=num, dist_method=dist, flip_dir=flip)
            curve_paths.append(path_fn())
        pu0, pu1, p0w, p1w = tuple(curve_paths)
        return pu0, pu1, p0w, p1w

    @property
    def mesh_points(self):
        """Returns surface mesh points."""
        pu0, pu1, p0w, p1w = self._get_curve_path_points()
        p00 = pu0[ 0, :]
        p11 = pu1[-1, :]
        p01 = p0w[-1, :]
        p10 = p1w[ 0, :]
        num_points_u, num_points_w = self.get_num_points()
        mp = np.zeros((3, num_points_u, num_points_w))
        for i, u in enumerate(np.linspace(0, 1, num=num_points_u, endpoint=True)):
            for j, w in enumerate(np.linspace(0, 1, num=num_points_w, endpoint=True)):
                p1 = (1-u)*p0w[j,:] + u*p1w[j,:]
                p2 = (1-w)*pu0[i,:] + w*pu1[i,:]
                p3 = (1-u)*(1-w)*p00 + u*(1-w)*p10 + (1-u)*w*p01 + u*w*p11
                for k in range(0, 3):
                    mp[k,i,j] = p1[k] + p2[k] - p3[k]
        return mp

    @property
    def panels(self):
        """Returns quadrilateral panels."""
        panels = []
        mp = self.mesh_points
        for j in range(0, mp.shape[2]-1):
            for i in range(0, mp.shape[1]-1):
                xyz1, xyz2, xyz3, xyz4 = mp[:,i,j], mp[:,i+1,j], mp[:,i+1,j+1], mp[:,i,j+1]
                panels.append([xyz1[0], xyz1[1], xyz1[2], 
                               xyz2[0], xyz2[1], xyz2[2], 
                               xyz3[0], xyz3[1], xyz3[2], 
                               xyz4[0], xyz4[1], xyz4[2]])
        return panels
