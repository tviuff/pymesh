"""Module containing Point classes.
"""

import math
from typing import Self

import numpy as np

from pymesh.descriptors import AsNumber

# from pymesh.geo.vector3d import Vector3D
from pymesh.typing import NDArray3
from pymesh.utils import validate_move_parameters


class Point:
    """Takes positional arguments x, y, z as either type 'int' or 'float'."""

    x = AsNumber(return_type=float)
    y = AsNumber(return_type=float)
    z = AsNumber(return_type=float)

    def __init__(self, x: int | float, y: int | float, z: int | float) -> None:
        self.x, self.y, self.z = x, y, z

    @property
    def xyz(self) -> NDArray3[np.float64]:
        return np.array([self.x, self.y, self.z])

    def __eq__(self, other) -> bool:
        return np.all(self.xyz == other.xyz)

    def __ne__(self, other: object) -> bool:
        return not self.__eq__(other)

    def __add__(self, other):
        return self.xyz + other.xyz

    def __sub__(self, other):
        return self.xyz - other.xyz

    def __repr__(self):
        return f"{type(self).__name__}(x={self.x:.2f}, y={self.y:.2f}, z={self.z:.2f})"

    def copy(self) -> Self:
        return Point(self.x, self.y, self.z)

    def move(self, dx: int | float, dy: int | float, dz: int | float) -> None:
        validate_move_parameters(dx, dy, dz)
        self.x += float(dx)
        self.y += float(dy)
        self.z += float(dz)

    # ! Uot-comment due to circular import (Vector3D file has "import Point")
    # def rotate(self, axis: Vector3D, angle: int | float) -> None:
    #     pass

    # def mirror(self, plane: Vector3D) -> None:
    #     pass

    def get_distance(self, point: Self) -> float:
        """Returns the shortest distance between point instance and another point"""
        if not isinstance(point, Point):
            raise TypeError(f"point must be of type '{Point.__name__}'.")
        dx = self.x - point.x
        dy = self.y - point.y
        dz = self.z - point.z
        return math.sqrt(dx**2 + dy**2 + dz**2)

    def create_relative_point(
        self, dx: int | float = 0, dy: int | float = 0, dz: int | float = 0
    ) -> Self:
        """Creates a new point using relative positional arguments dx, dy, dz"""
        for value in (dx, dy, dz):
            if not isinstance(value, (int, float)):
                raise TypeError("Relative position must be of type 'float' or 'int'")
        if (dx == 0.0) and (dy == 0.0) and (dz == 0.0):
            raise ValueError("A non-zero relative position must be given")
        x = self.x + float(dx)
        y = self.y + float(dy)
        z = self.z + float(dz)
        return Point(x, y, z)
