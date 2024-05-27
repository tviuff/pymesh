from collections.abc import Callable
from typing import Self

import numpy as np

from pymesh.geo.curves.curve import Curve
from pymesh.geo.point import Point
from pymesh.typing import NDArray3
from pymesh.utils import validate_curve_path_parameters

NUM_POINTS = 1000

# ! change from .path() to .get_path(), so we can create a path attribute
# ! in this class __init__...


class UserDefinedCurve(Curve):
    """Generic curve with a user defined path function.

    For more information, see Curve documentation.
    """

    def __init__(self, path: Callable[[float], tuple[float, float, float]]):
        """Initialization method.

        Args:
            path (Callable): User-defined curve path function,
                that takes a float between 0 and 1 and returns
                a tuple with three floats representing the x,
                y and z values of the point on the path corresponding
                to the input path ratio.
        """
        self._path = path

    def __eq__(self, other):
        is_equal = True
        if type(self).__name__ != type(other).__name__:
            is_equal = False
        else:
            for u in np.linspace(0, 1, num=NUM_POINTS, endpoint=True):
                xyz1 = self.path(u)
                xyz2 = other.path(u)
                if xyz1 != xyz2:
                    is_equal = False
                    break
        return is_equal

    def __ne__(self, other):
        return not self.__eq__(other)

    def __repr__(self):
        txt = f"{type(self).__name__}(path=UserDefined)"
        return txt

    @property
    def start(self) -> NDArray3[np.float64]:
        x, y, z = self.path(0)
        return Point(x, y, z)

    @property
    def end(self) -> NDArray3[np.float64]:
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
        return UserDefinedCurve(self._path)

    def move(
        self, dx: int | float = 0.0, dy: int | float = 0.0, dz: int | float = 0.0
    ) -> Self:
        raise NotImplementedError()

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
        raise NotImplementedError()

    def mirror(
        self,
        a: int | float,
        b: int | float,
        c: int | float,
        x0: int | float = 0.0,
        y0: int | float = 0.0,
        z0: int | float = 0.0,
    ) -> Self:
        raise NotImplementedError()
