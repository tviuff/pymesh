"""Module including the coons patch class
"""

import numpy as np

from gdfgen.surfaces import Surface
from gdfgen.curves import Curve
from gdfgen.mesh import DistributionMethod
from gdfgen.point import Point
from gdfgen.constants import MeshConstants as MConst

class CoonsPatch(Surface):
    """Coons patch class taking a selection of four curves
    and creates mesh points for generating panels.
    """

    __curve_selection:tuple[Curve]
    __dist_u0:DistributionMethod = MConst.DEFAULT_DIST_METHOD.value
    __dist_u1:DistributionMethod = MConst.DEFAULT_DIST_METHOD.value
    __dist_0w:DistributionMethod = MConst.DEFAULT_DIST_METHOD.value
    __dist_1w:DistributionMethod = MConst.DEFAULT_DIST_METHOD.value
    __mesh_points = None
    __num_points_u:int = MConst.DEFAULT_NUM_POINT.value
    __num_points_w:int = MConst.DEFAULT_NUM_POINT.value
    __panels = None
    __point00:Point
    __point01:Point
    __point10:Point
    __point11:Point

    def __init__(self, curve_u0:Curve, curve_u1:Curve, curve_0w:Curve, curve_1w:Curve):
        """Initializing Coons Patch curves."""
        curve_selection = (curve_u0, curve_u1, curve_0w, curve_1w)
        for curve in curve_selection:
            if not isinstance(curve, Curve):
                raise TypeError("Curve input must be of type 'Curve'.")
        if len(curve_selection) != 4:
            raise ValueError("Curve selection must consist of exactly four Curve instances.")
        self.__curve_selection = curve_selection
        passed, err = self._validate_curve_selectino()
        if not passed:
            raise err
        self.__point00 = curve_u0.point_start
        self.__point01 = curve_u1.point_start
        self.__point10 = curve_1w.point_start
        self.__point11 = curve_1w.point_end

    def _validate_curve_selectino(self):
        """Validates direction and intersection points of curve selection."""
        curve_u0, curve_u1, curve_0w, curve_1w = self.__curve_selection
        try:
            if not (curve_u0.point_start == curve_0w.point_start).all():
                raise ValueError(
                    "Curves 'curve_u0' and 'curve_0w' does not have the same starting point.")
            if not (curve_u1.point_end == curve_1w.point_end).all():
                raise ValueError( 
                    "Curves 'curve_u1' and 'curve_1w' does not have the same ending point.")
            if not (curve_u0.point_end == curve_1w.point_start).all():
                raise ValueError(
                    "Curve 'curve_u0' does not end where curve 'curve_1w' starts.")
            if not (curve_u1.point_start == curve_0w.point_end).all():
                raise ValueError(
                    "Curve 'curve_0w' does not end where curve 'curve_u1' starts.")
        except ValueError as err:
            return False, err
        return True, None

    def set_dist_methods(self,
            dist_u0:DistributionMethod=MConst.DEFAULT_DIST_METHOD.value,
            dist_u1:DistributionMethod=MConst.DEFAULT_DIST_METHOD.value,
            dist_0w:DistributionMethod=MConst.DEFAULT_DIST_METHOD.value,
            dist_1w:DistributionMethod=MConst.DEFAULT_DIST_METHOD.value,
        ):
        """Specifies curve path distribution methods, default is 'linear'."""
        self.__dist_u0 = dist_u0
        self.__dist_u1 = dist_u1
        self.__dist_0w = dist_0w
        self.__dist_1w = dist_1w

    def _get_dist_methods(self):
        """Returns curve path point distribution methods."""
        return self.__dist_u0, self.__dist_u1, self.__dist_0w, self.__dist_1w

    def set_num_points(self,
            num_points_u:int=MConst.DEFAULT_NUM_POINT.value,
            num_points_w:int=MConst.DEFAULT_NUM_POINT.value
        ):
        """Specify number of points along normalized u and w dimensions."""
        self.__num_points_u = num_points_u
        self.__num_points_w = num_points_w

    def _get_num_points(self):
        """Returns number of points along u and w dimensions."""
        return self.__num_points_u, self.__num_points_w

    def _get_curve_path_points(self):
        """Returns path points for each of the four input curves."""
        curve_paths = []
        num_points_u, num_points_w = self._get_num_points()
        num_points = (num_points_u, num_points_u, num_points_w, num_points_w)
        for curve, num, dist in zip(self.__curve_selection, num_points, self._get_dist_methods()):
            path_fn = curve.get_path_fn()
            curve_paths.append(path_fn(num, dist))
        pu0, pu1, p0w, p1w = tuple(curve_paths)
        return pu0, pu1, p0w, p1w

    def _set_mesh_points(self):
        """Generates surface mesh points in the physical x - y - z space."""
        pu0, pu1, p0w, p1w = self._get_curve_path_points()
        p00 = self.__point00.xyz
        p11 = self.__point11.xyz
        p01 = self.__point01.xyz
        p10 = self.__point10.xyz
        num_points_u, num_points_w = self._get_num_points()
        mp = np.zeros((3, num_points_u, num_points_w))
        for i, u in enumerate(np.linspace(0, 1, num=num_points_u, endpoint=True)):
            for j, w in enumerate(np.linspace(0, 1, num=num_points_w, endpoint=True)):
                p1 = (1-u)*p0w[j,:] + u*p1w[j,:]
                p2 = (1-w)*pu0[i,:] + w*pu1[i,:]
                p3 = (1-u)*(1-w)*p00 + u*(1-w)*p10 + (1-u)*w*p01 + u*w*p11
                for k in range(0, 3):
                    mp[k,i,j] = p1[k] + p2[k] - p3[k]
        self.__mesh_points = mp

    @property
    def mesh_points(self):
        """Returns surface mesh points."""
        if self.__mesh_points is None:
            self._set_mesh_points()
        return self.__mesh_points

    def _set_panels(self):
        """Generates Geometric Data File (GDF) panels."""
        panels = []
        mp = self.mesh_points
        for j in range(0, mp.shape[2]-1):
            for i in range(0, mp.shape[1]-1):
                xyz1, xyz2, xyz3, xyz4 = mp[:,i,j], mp[:,i+1,j], mp[:,i+1,j+1], mp[:,i,j+1]
                panels.append([xyz1[0], xyz1[1], xyz1[2], 
                               xyz2[0], xyz2[1], xyz2[2], 
                               xyz3[0], xyz3[1], xyz3[2], 
                               xyz4[0], xyz4[1], xyz4[2]])
        self.__panels = panels

    @property
    def panels(self):
        """Returns Geometric Data File (GDF) panels."""
        if self.__panels is None:
            self._set_panels()
        return self.__panels
