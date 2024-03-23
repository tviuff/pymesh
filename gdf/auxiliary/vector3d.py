"""Module including line class
"""

import numpy as np
from numpy import ndarray

from gdf.auxiliary.point import Point

# ! add vector math operations for easy use in the rest of the code

class Vector3D:
    """3d vector generated from two points in space"""

    def __init__(self, point_start:Point, point_end:Point) -> None:
        self.point_start = point_start
        self.point_end = point_end

    def __eq__(self, other):
        return (self.unit_vector == other.unit_vector).any() \
            and self.length == other.length

    def __repr__(self):
        vector = self.unit_vector * self.length
        txt = f"{type(self).__name__}(dx={vector[0]}, " \
                f"dy={vector[1]}, dz={vector[1]})"
        return txt

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
