"""Module containing Point classes.
"""

import inspect
import math
from typing import Self

import numpy as np
from numpy import ndarray

class CartesianCoordinate:
    """Coordinate descriptor class"""

    def __set_name__(self, owner, name):
        self._name = name

    def __get__(self, instance, owner) -> float:
        return instance.__dict__[self._name]

    def __set__(self, instance, value):
        if not isinstance(value, (int, float)):
            raise TypeError(f"{self._name} must be of type 'int' or 'float'")
        instance.__dict__[self._name] = float(value)

class Point:
    """Creates and handles point coordinates"""

    x = CartesianCoordinate()
    y = CartesianCoordinate()
    z = CartesianCoordinate()

    def __init__(self, x:int|float, y:int|float, z:int|float) -> None:
        self.x, self.y, self.z = x, y, z

    @property
    def xyz(self) -> ndarray:
        return np.array([self.x, self.y, self.z])

    def __eq__(self, other):
        return (self.xyz == other.xyz).all()

    def __repr__(self):
        return f"{type(self).__name__}(x={self.x:.2f}, y={self.y:.2f}, z={self.z:.2f})"

    @classmethod
    def get_distance(cls, point1:Self, point2:Self) -> float:
        """Returns the shortest distance between to points"""
        if not (isinstance(point1, cls) and isinstance(point2, cls)):
            cls_name = cls.__name__
            mth_name = inspect.stack()[0][3]
            raise TypeError(f"{cls_name}.{mth_name}() only takes arguments of type '{cls_name}'.")
        dx = point1.x - point2.x
        dy = point1.y - point2.y
        dz = point1.z - point2.z
        return math.sqrt(dx**2 + dy**2 + dz**2)

    @classmethod
    def set_relative_to(cls,
            point:Self = None,
            dx:int|float = 0.0,
            dy:int|float = 0.0,
            dz:int|float = 0.0
        ) -> Self:
        """Creates a new point using relative position"""
        if point is None:
            raise ValueError("Input must include a point reference.")
        if not isinstance(point, cls):
            raise TypeError(f"Input point reference must be of type '{cls.__name__}'.")
        if not isinstance(dx, (float, int)):
            raise TypeError("dx must be of type 'float' or 'int'.")
        if not isinstance(dy, (float, int)):
            raise TypeError("dy must be of type 'float' or 'int'.")
        if not isinstance(dz, (float, int)):
            raise TypeError("dz must be of type 'float' or 'int'.")
        if (dx == 0.0) and (dy == 0.0) and (dz == 0.0):
            raise ValueError("Input must include a non-zero relative distance.")
        x = point.x + float(dx)
        y = point.y + float(dy)
        z = point.z + float(dz)
        return cls(x, y, z)
