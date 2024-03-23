"""Module including abstract curve class
"""

from abc import ABC, abstractmethod

from gdf.auxiliary.point import Point

class Curve(ABC):
    """Curve abstract base class"""

    @property
    @abstractmethod
    def point_start(self) -> Point:
        """returns start point"""

    @property
    @abstractmethod
    def point_end(self) -> Point:
        """returns end point"""

    @property
    @abstractmethod
    def length(self) -> float:
        """Returns the curve path length"""

    @abstractmethod
    def get_path_fn(self, flip_direction:bool=False):
        """Returns curve path function that takes a float between 0 and 1
        and returns xyz coordinates as an ndarray with shape [1, 3]"""

    @staticmethod
    def _validate_curve_path_fn_input(u:int|float, flip_direction:bool) -> float:
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
