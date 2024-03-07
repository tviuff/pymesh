"""Module including surface and coons patch classes
"""

from typing import Protocol

class Surface(Protocol):
    """Abstract surface class
    """
    __mesh_points = None
    __panels = None
    def set_mesh_points(self):
        """Generates surface mesh points and set it to attribute"""
    def get_mesh_points(self):
        """Returns mesh_points from surface mesh"""
    def set_panels(self):
        """Generates panels from surface mesh and set it to attribute"""
    def get_panels(self):
        """Returns panels from surface mesh"""
