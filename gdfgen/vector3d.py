"""Module including line class
"""

import numpy as np
from numpy import ndarray

from gdfgen.points import Point

class Vector3D:
    """3d vector generated from two points in space"""

    def __init__(self, point_start:Point, point_end:Point) -> None:
        self.point_start = point_start
        self.point_end = point_end

    @property
    def point_start(self) -> Point:
        return self._point_start

    @point_start.setter
    def point_start(self, value:Point) -> None:
        if not isinstance(value, Point):
            raise TypeError("point_start must be of type 'Point'")
        self._point_start = value

    @property
    def point_end(self) -> Point:
        return self._point_end

    @point_end.setter
    def point_end(self, value:Point) -> None:
        if not isinstance(value, Point):
            raise TypeError("point_end must be of type 'Point'")
        self._point_end = value

    @property
    def length(self) -> float:
        return np.sqrt(np.sum((self.point_end.xyz-self.point_start.xyz)**2))

    @property
    def unit_vector(self) -> ndarray:
        return (self.point_end.xyz-self.point_start.xyz)/self.length
