"""Module including abstract curve class
"""

from typing import Protocol

from gdfgen.point import Point

class CurveInstance(Protocol):
    """Abstract curve class"""

    point_start:Point
    point_end:Point

    def get_path_fn():
        """Returns curve path algorithm"""

class Curve(CurveInstance):
    """Curve parent class for later inheritance"""

    def __init__(self, point_start:Point, point_end:Point) -> None:
        self.point_start = point_start
        self.point_end = point_end
