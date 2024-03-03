"""Module including curve and line classes
"""

import numpy as np

from .points import Point
from .constants import DIST_METHOD_FUNCTIONS, DEFAULT_DIST_METHOD

class Line:
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

    def get_points(self, n:int=10, method:str=DEFAULT_DIST_METHOD):
        """Distributes n internal points along based on a selected method.
        The method options are:
            'linear'     : linearly spaced.
            'cosine_both': increasingly more closely spaced at the ends.
            'cosine_end1': increasingly more closely spaced at end1.
            'cosine_end2': increasingly more closely spaced at end2.
        """
        assert (isinstance(n, int) and n > 1), "n must be a positive integer larger than 1."
        assert (method in DIST_METHOD_FUNCTIONS), f"'{method}' distribution method not recognized."
        xyz = np.zeros((n, 3))
        dist_function = DIST_METHOD_FUNCTIONS[method]
        for i, u in enumerate(np.linspace(0, 1, n, endpoint=True)):
            xyz[i, :] = self.p0.xyz + (self.p1.xyz - self.p0.xyz) * dist_function(u)
        return xyz
