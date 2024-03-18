"""Module including abstract curve class
"""

from abc import ABC, abstractmethod

from numpy import ndarray

from gdf.points import Point
from gdf.mesh.distribution_methods import DistMethod
from gdf.constants import MeshConstants

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
    def get_path_xyz(self,
        num_points:int, dist_method:DistMethod, flip_dir:bool=False) -> ndarray:
        """Returns curve path xyz points as a numpy array"""
