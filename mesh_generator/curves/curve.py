"""Module including abstract curve class
"""

from typing import Protocol

from ..mesh import DistributionMethod
from ..point import Point

class CurvePath(Protocol):
    """Abstract curve class
    """
    point_start:Point
    point_end:Point
    def get_path_fn(num_points:int, dist_method:DistributionMethod):
        """Returns curve path algorithm"""

class Curve(CurvePath):
    """Curve class"""
