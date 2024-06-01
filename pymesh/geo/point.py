import math
from typing import Self

import numpy as np

from pymesh.descriptors import AsNumber
from pymesh.typing import NDArray3
from pymesh.utils import rotate_point_xyz, mirror_point_xyz


class Point:
    """Point class with xyz coordinates in three-dimensional space.

    Attributes:
        x (int | float): Point x coordinate.
        y (int | float): Point y coordinate.
        z (int | float): Point z coordinate.
        xyz (NDArray3[float]): Numpy ndarray with x, y and z values.
            The numpy ndarray has shape (3,) with x at index 0, y at
            index 1 and z at index 2.
    """

    x = AsNumber(return_type=float)
    y = AsNumber(return_type=float)
    z = AsNumber(return_type=float)

    def __init__(self, x: int | float, y: int | float, z: int | float) -> None:
        """Initialization method.

        Args:
            x: Point x coordinate.
            y: Point y coordinate.
            z: Point z coordinate.
        """
        self.x, self.y, self.z = x, y, z

    @property
    def xyz(self) -> NDArray3[np.float64]:
        return np.array([self.x, self.y, self.z])

    def __eq__(self, other) -> bool:
        DECIMALS = 10
        return np.all(
            np.round(self.xyz, decimals=DECIMALS)
            == np.round(other.xyz, decimals=DECIMALS)
        )

    def __ne__(self, other: object) -> bool:
        return not self.__eq__(other)

    def __add__(self, other):
        return self.xyz + other.xyz

    def __sub__(self, other):
        return self.xyz - other.xyz

    def __repr__(self):
        return f"{type(self).__name__}(x={self.x:.2f}, y={self.y:.2f}, z={self.z:.2f})"

    def copy(self) -> Self:
        """Returns a copy of point instance"""
        return Point(self.x, self.y, self.z)

    def move(self, dx: int | float, dy: int | float, dz: int | float) -> Self:
        """Moves the point coordinates in space.

        Args:
            dx: Distance moved in the x-direction.
            dy: Distance moved in the y-direction.
            dz: Distance moved in the z-direction.

        Returns:
            (Point): Point with updated xyz coordinates.
        """
        for val in (dx, dy, dz):
            if not isinstance(val, (int, float)):
                raise TypeError(f"Expected {val!r} to be an int or float")
        self.x += float(dx)
        self.y += float(dy)
        self.z += float(dz)
        return self

    def rotate(
        self,
        angle: int | float,
        a: int | float,
        b: int | float,
        c: int | float,
        x0: int | float = 0.0,
        y0: int | float = 0.0,
        z0: int | float = 0.0,
    ) -> Self:
        """Rotates point around an axis.

        Parameters are passed to [pymesh.utils.rotate_point_xyz][].
        """
        self.x, self.y, self.z = rotate_point_xyz(
            self.x, self.y, self.z, angle, a, b, c, x0, y0, z0
        )
        return self

    def mirror(
        self,
        a: int | float,
        b: int | float,
        c: int | float,
        x0: int | float = 0.0,
        y0: int | float = 0.0,
        z0: int | float = 0.0,
    ) -> Self:
        """Mirrors point in a plane.

        Parameters are passed to [pymesh.utils.mirror_point_xyz][].
        """
        self.x, self.y, self.z = mirror_point_xyz(
            self.x, self.y, self.z, a, b, c, x0, y0, z0
        )
        return self

    def get_distance_to(self, point: Self) -> float:
        """Returns the shortest distance between point instance and another point

        Args:
            point: Other point from which the distance is calculated.

        Returns:
            (float): Direct distance between this and other point.

        Raises:
            TypeError: If point is not of type Self.
        """
        if not isinstance(point, Point):
            raise TypeError(f"point must be of type '{Point.__name__}'.")
        dx = self.x - point.x
        dy = self.y - point.y
        dz = self.z - point.z
        return math.sqrt(dx**2 + dy**2 + dz**2)

    def create_relative_point(
        self, dx: int | float = 0, dy: int | float = 0, dz: int | float = 0
    ) -> Self:
        """Creates a new point using relative positional arguments.

        Args:
            dx: Relative x coordinate.
            dy: Relative y coordinate.
            dz: Relative z coordinate.

        Returns:
            (Point): New point based on relative coordinates.

        Raises:
            TypeError: If dx, dy or dz are not of type int or float.
            ValueError: If both dx, dy and dz are equal to zero.
        """
        for value in (dx, dy, dz):
            if not isinstance(value, (int, float)):
                raise TypeError("Relative position must be of type 'float' or 'int'")
        if (dx == 0.0) and (dy == 0.0) and (dz == 0.0):
            raise ValueError("A non-zero relative position must be given")
        x = self.x + float(dx)
        y = self.y + float(dy)
        z = self.z + float(dz)
        return Point(x, y, z)
