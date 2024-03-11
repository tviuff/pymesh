"""Module including surface and coons patch classes
"""

from abc import ABC, abstractmethod

class Surface(ABC):
    """Surface class protocol
    """

    @property
    @abstractmethod
    def mesh_points(self):
        """Returns mesh_points from surface mesh"""

    @property
    @abstractmethod
    def panels(self):
        """Returns panels from surface mesh"""
