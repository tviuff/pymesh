"""Module including abstract curve class
"""

from abc import ABC, abstractmethod

from gdfgen.point import Point
from gdfgen.mesh import DistMethod

class Curve(ABC):
    """Curve abstract base class"""

    def __init__(self, point_start:Point, point_end:Point) -> None:
        self.point_start, self.point_end = point_start, point_end

    @property
    def point_start(self) -> Point:
        return self._point_start

    @point_start.setter
    def point_start(self, point:Point) -> None:
        if not isinstance(point, Point):
            raise TypeError("point_start must be of type 'Point'")
        self._point_start = point

    @property
    def point_end(self) -> Point:
        return self._point_end

    @point_end.setter
    def point_end(self, point:Point) -> None:
        if not isinstance(point, Point):
            raise TypeError("point_end must be of type 'Point'")
        self._point_end = point

    @abstractmethod
    def get_path_fn(self, num_points:int, dist_method:DistMethod, flip_dir:bool=False):
        """Returns curve path algorithm"""
