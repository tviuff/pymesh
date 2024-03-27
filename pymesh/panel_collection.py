"""Module containing PanelColletion class"""

import numpy as np

from pymesh.geo.vector3d import Vector3D


class PanelColletion:
    """Surface mesh generator"""

    def __init__(self, panels: list[list[float]]):
        self.panels = panels

    def move(
        self, dx: int | float = 0.0, dy: int | float = 0.0, dz: int | float = 0.0
    ) -> None:
        """Moves panel collection"""

    def rotate(self, axis: Vector3D, angle: int | float) -> None:
        """Rotates panel collection an angle around an axis vector"""

    def mirror(self, plane: Vector3D, angle: int | float) -> None:
        """Rotates panel collection an angle around an axis vector"""
