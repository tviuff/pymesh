"""Module containing theCurve class"""

from abc import ABC, abstractmethod
from collections.abc import Callable
from typing import Self

import numpy as np

from pymesh.geo.point import Point
from pymesh.geo.vector3d import Vector3D
from pymesh.descriptors import AsInstanceOf
from pymesh.typing import NDArray3


class Curve(ABC):
    """Curve abstract base class"""

    start = AsInstanceOf(Point)
    end = AsInstanceOf(Point)

    @abstractmethod
    def copy(self) -> Self:
        """Returns a copy of the curve object"""

    @abstractmethod
    def move(
        self, dx: int | float = 0.0, dy: int | float = 0.0, dz: int | float = 0.0
    ) -> None:
        """Moves the curve a given relative position"""

    @abstractmethod
    def rotate(self, axis: Vector3D, angle: int | float) -> None:
        """Rotates the curve around an axis.

        axis: vector axis the rotation is performed around

        angle: defined in radians with poitive diriction being
        counter-clockwise, based on the right-hand rule
        """

    @property
    @abstractmethod
    def length(self) -> float:
        """Returns the curve path length"""

    @abstractmethod
    def path(self, u: int | float, flip: bool = False) -> NDArray3[np.float64]:
        """Curve path function that returns a physical point in space.

        u:
        normalized path parameter between 0 and 1

        flip:
        Optional, if True then u = (1 - u), i.e. the direction is flipped

        return:
        numpy ndarray with shape (3, )
        """

    def get_path(self) -> Callable[[int | float, bool], NDArray3[np.float64]]:
        """Returns surface path function"""
        return self.path
