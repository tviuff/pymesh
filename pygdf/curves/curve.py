"""Module including abstract curve class
"""

from abc import ABC, abstractmethod

from numpy import ndarray

from pygdf.auxiliary.point import Point
from pygdf.descriptors import AsInstanceOf, AsNDArray

# ! Consider removing point_start_point_end and only store .length and .path()


class Curve(ABC):
    """Curve abstract base class"""

    start = AsNDArray(shape=(3,))
    end = AsNDArray(shape=(3,))

    point_start = AsInstanceOf(Point)
    point_end = AsInstanceOf(Point)

    @property
    @abstractmethod
    def length(self) -> float:
        """Returns the curve path length"""

    @abstractmethod
    def path(self, u: int | float) -> ndarray:
        """Curve path function that returns a physical point in space.

        u:
        normalized path parameter between -1 and 1.
        If positive, u is the percentage of the path covered
        If negative, the value is added to 1, i.e. the direction is flipped

        return:
        numpy ndarray with shape (3, )
        """

    @abstractmethod
    def get_path_fn(self, flip_direction: bool = False):
        """Returns curve path function that takes a float between 0 and 1
        and returns xyz coordinates as an ndarray with shape [1, 3]"""


def validate_path_parameter(u: int | float) -> float:
    """Validates the normalized curve path parameter.

    u:
    normalized path parameter between -1 and 1.
    If positive, u is the percentage of the path covered
    If negative, the value is added to 1, i.e. the direction is flipped

    return:
    u
    """
    if not isinstance(u, (int, float)):
        raise TypeError(f"Expected an int or float number, but got {u!r}")
    if isinstance(u, int):
        u = float(u)
    if u < -1 or 1 < u:
        raise ValueError(f"Expected a value between -1 and 1 but got {u!r}")
    if u < 0:
        u += 1
    return u


def validate_curve_path_input(u: int | float, flip_direction: bool) -> float:
    """Validates and modifies input if needed"""
    if not isinstance(u, (int, float)):
        raise TypeError("u must be of type 'int' or 'float'")
    if not isinstance(flip_direction, bool):
        raise TypeError("flip_direction must be of type 'bool'")
    if isinstance(u, int):
        u = float(u)
    if u < 0 or u > 1:
        raise ValueError("u must be a value between 0 and 1")
    if flip_direction:
        u = 1.0 - u
    return u
