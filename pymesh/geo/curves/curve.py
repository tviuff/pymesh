"""Module including abstract curve class
"""

from abc import ABC, abstractmethod
from collections.abc import Callable
from typing import Self

import numpy as np

from pymesh.descriptors import AsNDArray
from pymesh.typing import NDArray3


class Curve(ABC):
    """Curve abstract base class"""

    start = AsNDArray(shape=(3,))
    end = AsNDArray(shape=(3,))

    @abstractmethod
    def copy(self) -> Self:
        """Returns a copy of the curve object"""

    @abstractmethod
    def move(
        self, dx: int | float = 0.0, dy: int | float = 0.0, dz: int | float = 0.0
    ) -> None:
        """Moves the curve a given relative position"""

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
