"""Module including abstract curve class
"""

from typing import Protocol

from ..point import Point

class CurveInstance(Protocol):
    """Abstract curve class"""

    point_start:Point
    point_end:Point

    def get_path_fn():
        """Returns curve path algorithm"""

class Curve(CurveInstance):
    """Curve class"""

    def __init__(self, point_start:Point, point_end:Point):
        if not (isinstance(point_start, Point) and isinstance(point_end, Point)):
            raise TypeError("Curve class only takes point input of type 'Point'.")
        self.point_start = point_start
        self.point_end = point_end
