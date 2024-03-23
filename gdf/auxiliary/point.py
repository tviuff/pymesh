"""Module containing Point classes.
"""

import math
from typing import Self

import numpy as np
from numpy import ndarray

from gdf.descriptors import AsNumber

class Point:
    """Point class.
    
    Takes positional arguments x, y, z as either type 'int' or 'float'.
    """

    x = AsNumber(return_type=float)
    y = AsNumber(return_type=float)
    z = AsNumber(return_type=float)

    def __init__(self, x:int|float, y:int|float, z:int|float) -> None:
        self.x, self.y, self.z = x, y, z

    @property
    def xyz(self) -> ndarray:
        return np.array([self.x, self.y, self.z])

    def __eq__(self, other):
        return (self.xyz == other.xyz).all()

    def __repr__(self):
        return f"{type(self).__name__}(x={self.x:.2f}, y={self.y:.2f}, z={self.z:.2f})"

    def get_distance(self, point:Self) -> float:
        """Returns the shortest distance between point instance and another point"""
        if not isinstance(point, Point):
            raise TypeError(f"point must be of type '{Point.__name__}'.")
        dx = self.x - point.x
        dy = self.y - point.y
        dz = self.z - point.z
        return math.sqrt(dx**2 + dy**2 + dz**2)

    def create_relative_point(self, dx:int|float=0.,dy:int|float=0.,dz:int|float=0.) -> Self:
        """Creates a new point using relative positional arguments dx, dy, dz"""
        for value in (dx, dy, dz):
            if not isinstance(value, (float, int)):
                raise TypeError("relative position must be of type 'float' or 'int'")
        if (dx == 0.0) and (dy == 0.0) and (dz == 0.0):
            raise ValueError("a non-zero relative position must be given")
        x = self.x + float(dx)
        y = self.y + float(dy)
        z = self.z + float(dz)
        return Point(x, y, z)
