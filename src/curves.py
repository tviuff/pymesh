"""Module including curve and line classes
"""

import math
import numpy as np
from .points import Point
from .exceptions import NonUniqueInputError

class Line:
    """Line generated from two points in space
    """
    def __init__(self, p0: Point, p1: Point):
        if p0 == p1:
            raise NonUniqueInputError(f"input points p0 {p0} and p1 {p1} must not identical.")
        self.p0, self.p1 = p0, p1

    def __eq__(self, other):
        return self.p0 == other.p0 and self.p1 == other.p1

    def __repr__(self):
        return f"{self.__class__.__name__}({self.p0}, {self.p1})"

    def get_points(self, n:int=10, method="linear"):
        """Generates n internal points along the line using linear, cosine, cos01 and cos10 methods
        """
        assert (n > 1), f"N {n} is not larger than 1."
        assert (method in ["linear", "cosine", "cos01", "cos10"]), \
            f"method {method} not recognized."
        xyz = np.zeros((n, 3))
        for i, u in enumerate(np.linspace(0, 1, n, endpoint=True)):
            if method == "cosine":
                uu = math.cos(math.pi*(1 - u))/2 + 0.5
            elif method == "cos01":
                uu = math.cos(math.pi*u/2)
            elif method == "cos10":
                uu = 1-math.cos(math.pi*u/2)
            else:
                uu = u
            xyz[i,:] = self.p0.xyz + (self.p1.xyz - self.p0.xyz)*uu
        return xyz
