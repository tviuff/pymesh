"""Module containing Point classes.
"""

import math
import inspect
from typing import TypeVar

import numpy as np

T = TypeVar("T")

class Point[T]:
    """Creates and handles point coordinates
    """

    def __init__(self, x:float|int, y:float|int, z:float|int):
        for arg in (x, y, z):
            if not isinstance(arg, (float, int)):
                raise TypeError(f"{self.__class__.__name__}.__init__() only takes arguments of type 'float' or 'int'.")
        self.x, self.y, self.z = float(x), float(y), float(z)
        self.xyz = np.array([self.x, self.y, self.z])

    def __eq__(self, other):
        return (self.xyz == other.xyz).all()

    def __repr__(self):
        return f"{self.__class__.__name__}({self.x:.2f}, {self.y:.2f}, {self.z:.2f})"

    @classmethod
    def get_distance(cls, point1:T, point2:T) -> float:
        """Returns the distance between to points.
        """
        if not (isinstance(point1, Point) and isinstance(point2, Point)):
            cls_name = cls.__name__
            mth_name = inspect.stack()[0][3]
            raise TypeError(f"{cls_name}.{mth_name}() only takes arguments of type '{cls_name}'.")
        dx = point1.x - point2.x
        dy = point1.y - point2.y
        dz = point1.z - point2.z
        return math.sqrt(dx**2 + dy**2 + dz**2)

    @classmethod
    def set_point_relative_to(cls, point:T=None, dx:float=0.0, dy:float=0.0, dz:float=0.0) -> T:
        """Creates a new point using relative position arguments (dx, dy, dz)
        to existing Point instance
        """
        if (point is None) and dx == 0.0 and dy == 0.0 and dz == 0.0:
            raise ValueError("Input must include a relative distance.")
        if not isinstance(point, Point):
            raise TypeError("Input point must of type 'Point'.")
        if not (isinstance(dx, (float, int)) \
                or isinstance(dy, (float, int)) \
                or isinstance(dz, (float, int))):
            raise TypeError("Relative position input must be of type 'float' or 'int'.")
        x = point.x + float(dx)
        y = point.y + float(dy)
        z = point.z + float(dz)
        return Point(x, y, z)
