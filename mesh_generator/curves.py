"""Module including curve and line classes
"""

import numpy as np

from .points import Point
from .mesh import Mesher

class Line(Mesher):
    """Line generated from two points in space
    """

    def __init__(self, p0: Point, p1: Point):
        assert(isinstance(p0, Point) and isinstance(p1, Point)), \
            "Line arguments must be instances of the Point class."
        assert(p0 != p1), "Line points must be unique."
        self.p0, self.p1 = p0, p1

    def __eq__(self, other):
        return self.p0 == other.p0 and self.p1 == other.p1

    def __repr__(self):
        return f"{self.__class__.__name__}({self.p0}, {self.p1})"

    def generate_mesh_points(self, num_points:int=10, option:str=None):
        """Generates 'num_point' mesh points along curve using a selected option.
        The options can be read by using the class method '.print_mesh_dist_option_list()'.
        """
        num_points = super()._validate_mesh_num_points(num_points)
        mesh_dist_func = super()._get_mesh_distribution_function(option)
        xyz = np.zeros((num_points, 3))
        for i, u in enumerate(np.linspace(0, 1, num_points, endpoint=True)):
            xyz[i, :] = self.p0.xyz + (self.p1.xyz - self.p0.xyz) * mesh_dist_func(u)
        return xyz
