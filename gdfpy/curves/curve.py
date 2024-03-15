"""Module including abstract curve class
"""

from abc import ABC, abstractmethod

from numpy import ndarray

from gdfpy.points import Point
from gdfpy.mesh import DistMethod
from gdfpy.constants import MeshConstants

class Curve(ABC):
    """Curve abstract base class"""

    def __init__(self, point_start:Point, point_end:Point) -> None:
        self.point_start = point_start
        self.point_end = point_end

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
    def get_path_xyz(self,
            num_points:int = MeshConstants.DEFAULT_NUM_POINT.value,
            dist_method:DistMethod = MeshConstants.DEFAULT_DIST_METHOD.value,
            flip_dir:bool = False
        ) -> ndarray:
        """Returns curve path xyz points as a numpy array"""
