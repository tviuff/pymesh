"""Module including the coons patch class
"""

import numpy as np

from ..surfaces import Surface
from ..curves import Curve
from ..mesh import DistributionMethod, Linear
from ..point import Point

class CoonsPatch(Surface):
    """Coons patch class taking a selection of four curves
    and creates mesh points for generating panels.
    """

    DEFAULT_NUM_POINT = 10
    DEFAULT_DIST_METHOD = Linear

    __curve_selection:tuple[Curve]
    __dist_u0:DistributionMethod = DEFAULT_DIST_METHOD
    __dist_u1:DistributionMethod = DEFAULT_DIST_METHOD
    __dist_0w:DistributionMethod = DEFAULT_DIST_METHOD
    __dist_1w:DistributionMethod = DEFAULT_DIST_METHOD
    __mesh_points = None
    __num_points_u:int = DEFAULT_NUM_POINT
    __num_points_w:int = DEFAULT_NUM_POINT
    __panels = None
    __point00:Point
    __point01:Point
    __point10:Point
    __point11:Point

    def __init__(self, curve_u0:Curve, curve_u1:Curve, curve_0w:Curve, curve_1w:Curve):
        """Initializing curves and points in the normalized u - w space.
        """
        curve_selection = (curve_u0, curve_u1, curve_0w, curve_1w)
        for curve in curve_selection:
            if not isinstance(curve, Curve):
                raise TypeError("curve_selection can only contain elements of type 'Curve'.")
        if len(curve_selection) != 4:
            raise ValueError("Curve selection must consist of exactly four Curve instances.")
        self.__curve_selection = curve_selection
        passed, err = self.__validate_curve_selection()
        if not passed:
            raise err
        self.__point00 = curve_u0.point_start
        self.__point01 = curve_u1.point_start
        self.__point10 = curve_1w.point_start
        self.__point11 = curve_1w.point_end

    def __validate_curve_selection(self):
        """Validates curve selection."""
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
            dist_u0:DistributionMethod=DEFAULT_DIST_METHOD,
            dist_u1:DistributionMethod=DEFAULT_DIST_METHOD,
            dist_0w:DistributionMethod=DEFAULT_DIST_METHOD,
            dist_1w:DistributionMethod=DEFAULT_DIST_METHOD,
        ):
        """Sets distribution methods. Default is 'linear'"""
        self.__dist_u0 = dist_u0
        self.__dist_u1 = dist_u1
        self.__dist_0w = dist_0w
        self.__dist_1w = dist_1w

    def get_dist_methods(self):
        """Returns distribution methods"""
        return self.__dist_u0, self.__dist_u1, self.__dist_0w, self.__dist_1w

    def set_num_points(self, num_points_u:int=DEFAULT_NUM_POINT, num_points_w:int=DEFAULT_NUM_POINT):
        """Specify number of points along u and w dimensions"""
        self.__num_points_u = num_points_u
        self.__num_points_w = num_points_w

    def get_num_points(self):
        """Returns number of points along u and w dimensions"""
        return self.__num_points_u, self.__num_points_w

    def set_mesh_points(self):
        """Generates surface mesh points in the non-parametric space.
        See also: https://youtu.be/TM0GM6xhAoI?t=2090 for more information.
        """
        num_points_u, num_points_w = self.get_num_points()
        dist_u0, dist_u1, dist_0w, dist_1w = self.get_dist_methods()
        curve_u0, curve_u1, curve_0w, curve_1w = self.__curve_selection
        fn_u0 = curve_u0.get_path_fn()
        fn_u1 = curve_u1.get_path_fn()
        fn_0w = curve_0w.get_path_fn()
        fn_1w = curve_1w.get_path_fn()
        pu0 = fn_u0(num_points_u, dist_u0)
        pu1 = fn_u1(num_points_u, dist_u1)
        p0w = fn_0w(num_points_w, dist_0w)
        p1w = fn_1w(num_points_w, dist_1w)
        p00 = self.__point00.xyz
        p11 = self.__point11.xyz
        p01 = self.__point01.xyz
        p10 = self.__point10.xyz
        mp = np.zeros((3, num_points_u, num_points_w))
        for i, u in enumerate(np.linspace(0, 1, num=num_points_u, endpoint=True)):
            for j, w in enumerate(np.linspace(0, 1, num=num_points_w, endpoint=True)):
                p1 = (1-u)*p0w[j,:] + u*p1w[j,:]
                p2 = (1-w)*pu0[i,:] + w*pu1[i,:]
                p3 = (1-u)*(1-w)*p00 + u*(1-w)*p10 + (1-u)*w*p01 + u*w*p11
                for k in range(0, 3):
                    mp[k,i,j] = p1[k] + p2[k] - p3[k]
        self.__mesh_points = mp

    def get_mesh_points(self):
        if self.__mesh_points is None:
            self.set_mesh_points()
        return self.__mesh_points

    def set_panels(self):
        if self.__mesh_points is None:
            _ = self.get_mesh_points()
        panels = []
        mp = self.__mesh_points
        for j in range(0, mp.shape[2]-1):
            for i in range(0, mp.shape[1]-1):
                xyz1, xyz2, xyz3, xyz4 = mp[:,i,j], mp[:,i+1,j], mp[:,i+1,j+1], mp[:,i,j+1]
                panels.append([xyz1[0], xyz1[1], xyz1[2], 
                               xyz2[0], xyz2[1], xyz2[2], 
                               xyz3[0], xyz3[1], xyz3[2], 
                               xyz4[0], xyz4[1], xyz4[2]])
        self.__panels = panels

    def get_panels(self):
        if self.__panels is None:
            self.set_panels()
        return self.__panels
