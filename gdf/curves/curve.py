"""Module including abstract curve class
"""

from abc import ABC, abstractmethod

from gdf.points import Point

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
    def get_path_fn(self):
        """Returns curve path function that takes a float between 0 and 1
        and returns xyz coordinates as an ndarray with shape [1, 3]"""
