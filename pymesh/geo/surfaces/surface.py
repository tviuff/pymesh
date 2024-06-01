from __future__ import annotations
from abc import ABC, abstractmethod
from collections.abc import Callable
from typing import Self

import numpy as np

from pymesh.other.typing import NDArray3


class Surface(ABC):
    """Abstract base class used which all surface classes inherit from.

    Attributes:
        is_normal_flipped (bool): Specifies surface normal direction.
    """

    _all_surfaces: list = []
    _is_normal_flipped: bool = False

    @property
    def is_normal_flipped(self) -> bool:
        return self._is_normal_flipped

    @classmethod
    def get_all_surfaces(cls) -> tuple[Surface]:
        """Returns a list of all generated surfaces, independent of surface class name."""
        return tuple(cls._all_surfaces)

    def flip_normal(self) -> Self:
        """Flips surface normal"""
        self._is_normal_flipped = not self._is_normal_flipped
        return self

    @abstractmethod
    def copy(self) -> Self:
        """Returns a recursive copy of surface instance."""

    @abstractmethod
    def move(
        self, dx: int | float = 0.0, dy: int | float = 0.0, dz: int | float = 0.0
    ) -> Self:
        """Moves the surface a given relative position in space.

        Args:
            dx: Distance moved in the x-direction.
            dy: Distance moved in the y-direction.
            dz: Distance moved in the z-direction.

        Returns:
            (Surface): Surface with updated xyz coordinates.

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
        """Rotates surface around an axis.

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
            (Surface): Rotated surface instance.

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
        """Mirrors surface in a plane.

        Plane is defined by a plane normal vector (a, b, c) and a point (x0, y0, z0) in the plane.
        Implementation based on formulation by [Jean Marie](https://math.stackexchange.com/questions/3927881/reflection-over-planes-in-3d).

        Args:
            a: Plane normal vector x dimension.
            b: Plane normal vector y dimension.
            c: Plane normal vector z dimension.
            x0: Plane normal vector base x coordinate
                Default is zero.
            y0: Plane normal vector base y coordinate
                Default is zero.
            z0: Plane normal vector base z coordinate
                Default is zero.

        Returns:
            (Surface): Mirrored surface instance.

        Raises:
            TypeError: If input value are not of type int or float.
        """

    def get_path(
        self,
    ) -> Callable[[int | float, int | float, bool, bool], NDArray3[np.float64]]:
        """Returns surface path function"""
        return self.path

    @abstractmethod
    def path(
        self, u: int | float, w: int | float, uflip: bool = False, wflip: bool = False
    ) -> NDArray3[np.float64]:
        """Surface path function that converts two normalized inputs u and w to a physical xyz point on the surface.

        Args:
            u: Normalized surface dimension path parameter between 0 and 1,
                where 0 and 1 represents the start and end locations, respectively.
            w: Normalized surface dimension path parameter between 0 and 1,
                where 0 and 1 represents the start and end locations, respectively.
            uflip: Defaults to False.
                If True then u = (1 - u), i.e. the direction is flipped.
            wflip: Defaults to False.
                If True then w = (1 - w), i.e. the direction is flipped.

        Returns:
            (NDArray3[float]): Numpy ndarray with shape (3,)

        Raises:
            TypeError: If u or w are not of type int or float.
            ValueError: If u or w are not part of the number set [0 1].
        """

    @abstractmethod
    def get_max_lengths(self) -> tuple[float]:
        """Returns a tuple of shape (2,) with the longest surface
        boundary length along each of the u and w dimensions. Indices
        0 and 1 represent the u and w dimensions, respectively.
        """
