"""Module including surface and coons patch classes
"""

from typing import Protocol

class Surface(Protocol):
    """Abstract surface class
    """

    __mesh_points = None
    __panels = None

    def _set_mesh_points():
        """Generates surface mesh points and set it to attribute"""

    @property
    def mesh_points():
        """Returns mesh_points from surface mesh"""

    def _set_panels():
        """Generates panels from surface mesh and set it to attribute"""

    @property
    def panels():
        """Returns panels from surface mesh"""
