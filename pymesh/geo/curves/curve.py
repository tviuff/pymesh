"""Module including abstract curve class
"""

from abc import ABC, abstractmethod
from collections.abc import Callable

import numpy as np

from pymesh.typing import NDArray3
from pymesh.descriptors import AsNDArray

# ! Consider removing point_start_point_end and only store .length and .path()


class Curve(ABC):
    """Curve abstract base class"""

    start = AsNDArray(shape=(3,))
    end = AsNDArray(shape=(3,))

    @property
    @abstractmethod
    def length(self) -> float:
        """Returns the curve path length"""

    def get_path(self) -> Callable[[int | float, bool], NDArray3[np.float64]]:
        """Returns surface path function"""
        return self.path

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


def validate_curve_path_parameters(u: int | float, flip: bool = False) -> float:
    """Validates the normalized curve path parameter.

    u:
    Normalized path parameter between 0 and 1

    flip:
    Optional, if True then u = (1 - u), i.e. the direction is flipped

    return:
    u
    """
    if not isinstance(u, (int, float)):
        raise TypeError(f"Expected an int or float number, but got {u!r}")
    if isinstance(u, int):
        u = float(u)
    if u < 0 or 1 < u:
        raise ValueError(f"Expected a value between 0 and 1 but got {u!r}")
    if flip:
        u = 1 - u
    return u
