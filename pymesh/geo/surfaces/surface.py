"""Module containing the Surface class"""

from __future__ import annotations
from abc import ABC, abstractmethod
from collections.abc import Callable
from typing import Self

import numpy as np

from pymesh.typing import NDArray3


class Surface(ABC):
    """Surface abstract class"""

    _all_surfaces: list = []
    _is_normal_flipped: bool = False

    @property
    def is_normal_flipped(self) -> bool:
        return self._is_normal_flipped

    @classmethod
    def get_all_surfaces(cls) -> tuple[Surface]:
        """Returns a list of all generated surfaces, independent of surface class name"""
        return tuple(cls._all_surfaces)

    def flip_normal(self) -> None:
        """Flips surface normal"""
        self._is_normal_flipped = not self._is_normal_flipped

    @abstractmethod
    def copy(self) -> Self:
        """Returns a recursive copy of surface instance"""

    @abstractmethod
    def move(
        self, dx: int | float = 0.0, dy: int | float = 0.0, dz: int | float = 0.0
    ) -> Self:
        """Moves the surface a given relative position"""

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
        """Rotates the curve around an axis.

        angle: defined in radians with poitive diriction being
        counter-clockwise, based on the right-hand rule.
        a, b, c: axis vector direction.
        x0, y0, z0: axis base, default is origin of coordinate system.
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

        Plane is defined by a normal vector (a, b, c) and a point (x0, y0, z0).
        By default x0 = 0.0, y0 = 0.0 and z0 = 0.0.
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
        """Surface path function that returns a point in physical space.

        u:
        Normalized path parameter between 0 and 1

        w:
        Normalized path parameter between 0 and 1

        uflip:
        Optional, if True then u = (1 - u), i.e. the direction is flipped

        wflip:
        Optional, if True then u = (1 - u), i.e. the direction is flipped

        return:
        u, w
        """

    @abstractmethod
    def get_max_lengths(self) -> tuple[float]:
        """Returns a tuple of shape (2,) with the longest surface
        boundary length along each of the u and w dimensions. Indices
        0 and 1 represent the u and w dimensions, respectively.
        """
