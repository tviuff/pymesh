from abc import ABC, abstractmethod
from collections.abc import Callable
from typing import Self

import numpy as np

from pymesh.geo.point import Point
from pymesh.descriptors import AsInstanceOf
from pymesh.typing import NDArray3


class Curve(ABC):
    """Abstract base class used which all curve classes inherit from.

    Attributes:
        start (Point): Curve starting point.
        end (Point): Curve ending point.
    """

    start = AsInstanceOf(Point)
    """Curve starting point."""

    end = AsInstanceOf(Point)
    """Curve ending point."""

    @abstractmethod
    def copy(self) -> Self:
        """Returns a recursive copy of curve instance."""

    @abstractmethod
    def move(
        self, dx: int | float = 0.0, dy: int | float = 0.0, dz: int | float = 0.0
    ) -> Self:
        """Moves the curve a given relative position in space.

        Args:
            dx: Distance moved in the x-direction.
            dy: Distance moved in the y-direction.
            dz: Distance moved in the z-direction.

        Returns:
            (Curve): Curve with updated xyz coordinates.

        Raises:
            TypeError: If dx, dy or dz are not of type int or float.
            ValueError: If dx, dy and dz are all zero.
        """

    @abstractmethod
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
        """Rotates curve around an axis.

        Implementation based on [WikiPedia](https://en.wikipedia.org/wiki/Rodrigues%27_rotation_formula).

        Args:
            angle: Angle in radians.
                Poitive direction defined as counter-clockwise, based on the right-hand rule.
            a: Axis vector x direction.
            b: Axis vector y direction.
            c: Axis vector z direction.
            x0: Axis base x coordinate
                Default is zero.
            y0: Axis base y coordinate
                Default is zero.
            z0: Axis base z coordinate
                Default is zero.

        Returns:
            (Curve): Rotated curve instance.

        Raises:
            TypeError: If input value are not of type int or float.
        """

    @abstractmethod
    def mirror(
        self,
        a: int | float,
        b: int | float,
        c: int | float,
        x0: int | float = 0.0,
        y0: int | float = 0.0,
        z0: int | float = 0.0,
    ) -> Self:
        """Mirrors curve in a plane.

        Plane is defined by a plane normal vector (a, b, c) and a point (x0, y0, z0) in the plane.
        Implementation based on formulation by [Jean Marie](https://math.stackexchange.com/questions/3927881/reflection-over-planes-in-3d).

        Args:
            a: Plane normal vector x dimension.
            b: Plane normal vector y dimension.
            c: Plane normal vector z dimension.
            x0: Plane normal vector base x coordinate
                Default is origin of coordinate system.
            y0: Plane normal vector base y coordinate
                Default is origin of coordinate system.
            z0: Plane normal vector base z coordinate
                Default is origin of coordinate system.

        Returns: Mirrored curve instance.

        Raises:
            TypeError: If input value are not of type int or float.
        """

    @property
    @abstractmethod
    def length(self) -> float:
        """Returns the curve path length"""

    @abstractmethod
    def path(self, u: int | float, flip: bool = False) -> NDArray3[np.float64]:
        """Curve path function that converts a normalized input u to a physical xyz point in space.

        Args:
            u: Normalized path parameter between 0 and 1,
                where 0 and 1 represents the start and end locations, respectively.
            flip: Bool specifying if path direction is flipped.
                If True then u = (1 - u), i.e. the direction is flipped. Defaults
                to False.

        Returns:
            (NDArray3): Numpy ndarray with shape (3,)

        Raises:
            TypeError: If u is not of type int or float.
            ValueError: If u is not part of the number set [0 1].
        """

    def get_path(self) -> Callable[[int | float, bool], NDArray3[np.float64]]:
        """Returns curve path function"""
        return self.path
