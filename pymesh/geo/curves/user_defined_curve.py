from collections.abc import Callable
from typing import Self
import copy

import numpy as np

from pymesh.geo.curves.curve import Curve
from pymesh.geo.point import Point
from pymesh.other.typing import NDArray3
from pymesh.other.utils import (
    validate_curve_path_parameters,
    rotate_point_xyz,
    mirror_point_xyz,
)

NUM_POINTS = 1000
TOLERANCE = 1e-3

# ! change from .path() to .get_path(), so we can create a path attribute
# ! in this class __init__...


class UserDefinedCurve(Curve):
    """Generic curve with a user defined path function.

    For more information, see Curve documentation.
    """

    def __init__(self, path: Callable[[int | float], NDArray3[np.float64]]):
        """Initialization method.

        Args:
            path (Callable): User-defined curve path function,
                that takes a float between 0 and 1 and returns
                a numpy.ndarray with shape (3,) and elements
                representing the x, y and z values of the point
                on the path corresponding to the input path ratio.
        """
        result = path(0)
        if not isinstance(result, np.ndarray):
            raise TypeError(
                f"Expected path function to return a numpy ndarray, but got {result!r}"
            )
        if not result.shape == (3,):
            raise TypeError(
                f"Expected path function to return a numpy ndarray of shape (3,), but got {result.shape}"
            )
        self._path = path

    def __eq__(self, other):
        is_equal = True
        if type(self).__name__ != type(other).__name__:
            is_equal = False
        else:
            for u in np.linspace(0, 1, num=NUM_POINTS, endpoint=True):
                xyz1 = self.path(u)
                xyz2 = other.path(u)
                if not np.isclose(xyz1, xyz2, atol=TOLERANCE).all():
                    is_equal = False
                    break
        return is_equal

    def __ne__(self, other):
        return not self.__eq__(other)

    def __repr__(self):
        txt = f"{type(self).__name__}(path=UserDefined)"
        return txt

    @property
    def start(self) -> Point:
        x, y, z = self.path(0)
        return Point(x, y, z)

    @property
    def end(self) -> Point:
        x, y, z = self.path(1)
        return Point(x, y, z)

    @property
    def length(self) -> float:
        distance = 0.0
        xyz0 = self.path(0)
        for u in np.linspace(start=0, stop=1, num=NUM_POINTS, endpoint=True):
            xyz1 = self.path(u)
            distance += np.sqrt(np.sum((xyz1 - xyz0) ** 2))
            xyz0 = xyz1
        return distance

    def path(self, u: int | float, flip: bool = False) -> NDArray3[np.float64]:
        u = validate_curve_path_parameters(u, flip)
        return self._path(u)

    def copy(self) -> Self:
        return UserDefinedCurve(copy.copy(self._path))

    def move(
        self, dx: int | float = 0.0, dy: int | float = 0.0, dz: int | float = 0.0
    ) -> Self:
        _path = copy.copy(self._path)

        def moved_path(u):
            return _path(u) + np.array([dx, dy, dz])

        self._path = moved_path
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
        _path = copy.copy(self._path)

        def rotated_path(u):
            x, y, z = _path(u)
            return rotate_point_xyz(x, y, z, angle, a, b, c, x0, y0, z0)

        self._path = rotated_path
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
        _path = copy.copy(self._path)

        def mirored_path(u):
            x, y, z = _path(u)
            return mirror_point_xyz(x, y, z, a, b, c, x0, y0, z0)

        self._path = mirored_path
        return self
