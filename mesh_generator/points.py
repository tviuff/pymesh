"""Module containing Point classes.
"""

import math
from typing import TypeVar

import numpy as np


T = TypeVar("T")

class Point[T]:
    """Creates and handles point coordinates
    """
    def __init__(self, x:float, y:float, z:float):
        assert(isinstance(x, float) and isinstance(y, float) and isinstance(z, float)), \
            "Point arguments must all be of type float."
        self.x = x
        self.y = y
        self.z = z
        self.xyz = np.array([x, y, z])

    def __eq__(self, other):
        return (self.xyz == other.xyz).all()

    def __repr__(self):
        return f"{self.__class__.__name__}({self.x:.2f}, {self.y:.2f}, {self.z:.2f})"

    @classmethod
    def get_distance(cls, p0:T, p1:T) -> float:
        """Returns the distance between to points.
        """
        dx = p1.x - p0.x
        dy = p1.y - p0.y
        dz = p1.z - p0.z
        return math.sqrt(dx**2 + dy**2 + dz**2)
