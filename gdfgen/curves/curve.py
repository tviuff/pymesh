"""Module including abstract curve class
"""

from abc import ABC, abstractmethod

from gdfgen.point import Point
from gdfgen.mesh import DistMethod

class Curve(ABC):
    """Curve abstract base class"""

    point_start:Point
    point_end:Point

    def __init__(self, point_start:Point, point_end:Point) -> None:
        self.point_start = point_start
        self.point_end = point_end

    @abstractmethod
    def get_path_fn(self, num_points:int, dist_method:DistMethod, flip_dir:bool=False):
        """Returns curve path algorithm"""
