"""Module including surface classes
"""

import numpy as np

from .curves import Line
from .mesh import SurfaceMesher

class CoonsPatch(SurfaceMesher):
    """Not yet working properly
    """
    def __init__(self, curve_u0:Line, curve_u1:Line, curve_0w:Line, curve_1w:Line):
        """Initializing curves and points in the parametric U-W space.
        """
        super().__init__()
        curve_selection = (curve_u0, curve_u1, curve_0w, curve_1w)
        passed, err = self.validate_curve_selection(curve_selection)
        if not passed:
            raise err
        self.curve_u0 = curve_u0 # BUG: instead save self.curve_selection and make an un_pack method
        self.curve_u1 = curve_u1
        self.curve_0w = curve_0w
        self.curve_1w = curve_1w
        self.point00 = self.curve_u0.start
        self.point01 = self.curve_u1.start
        self.point10 = self.curve_1w.start
        self.point11 = self.curve_1w.end

    @classmethod
    def validate_curve_selection(cls, curve_selection:tuple):
        """Validates curve selection."""
        curve_u0, curve_u1, curve_0w, curve_1w = curve_selection
        try:
            if not (curve_u0.start == curve_0w.start).all():
                raise ValueError(
                    "Curves 'curve_u0' and 'curve_0w' does not have the same starting point.")
            if not (curve_u1.end == curve_1w.end).all():
                raise ValueError( 
                    "Curves 'curve_u1' and 'curve_1w' does not have the same ending point.")
            if not (curve_u0.end == curve_1w.start).all():
                raise ValueError(
                    "Curve 'curve_u0' does not end where curve 'curve_1w' starts.")
            if not (curve_u1.start == curve_0w.end).all():
                raise ValueError(
                    "Curve 'curve_0w' does not end where curve 'curve_u1' starts.")
        except ValueError as err:
            return False, err
        return True, None

    def generate_mesh_points(self,
        num_points_u:int=10, num_points_w:int=10,
        option_u0:str=None, option_u1:str=None,
        option_0w:str=None, option_1w:str=None
        ):
        """Generates surface mesh points in the non-parametric space.
        See also: https://youtu.be/TM0GM6xhAoI?t=2090 for more information.
        
        For list of possible options use CurveMesher.print_mesh_dist_option_list()
        """
        pu0 = self.curve_u0.generate_mesh_points(num_points_u, option_u0)
        pu1 = self.curve_u1.generate_mesh_points(num_points_u, option_u1)
        p0w = self.curve_0w.generate_mesh_points(num_points_w, option_0w)
        p1w = self.curve_1w.generate_mesh_points(num_points_w, option_1w)
        p00, p11, p01, p10 = self.point00.xyz, self.point11.xyz, self.point01.xyz, self.point10.xyz
        p = np.zeros((3, num_points_u, num_points_w))
        for i, u in enumerate(np.linspace(0, 1, num=num_points_u, endpoint=True)):
            for j, w in enumerate(np.linspace(0, 1, num=num_points_w, endpoint=True)):
                p1 = (1-u)*p0w[j,:] + u*p1w[j,:]
                p2 = (1-w)*pu0[i,:] + w*pu1[i,:]
                p3 = (1-u)*(1-w)*p00 + u*(1-w)*p10 + (1-u)*w*p01 + u*w*p11
                for k in range(0, 3):
                    p[k,i,j] = p1[k] + p2[k] - p3[k]
        self._mesh_points = p
