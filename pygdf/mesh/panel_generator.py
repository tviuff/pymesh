"""Module containing surface mesher class"""

from typing import Self

import numpy as np

from pygdf.auxiliary.point import Point
from pygdf.descriptors import AsInstanceOf, AsContainerOf
from pygdf.mesh.distributions import MeshDistribution, LinearDistribution
from pygdf.surfaces.surface import Surface
from pygdf.surfaces.bilinear_surface import BilinearSurface


class PanelGenerator:
    """Surface mesh / panel generator"""

    LENGTH: int = 2

    num_points = None
    mesh_points = None

    entity = AsInstanceOf(Surface)
    mesh_distributions = AsContainerOf(
        container_type=tuple,
        item_type=MeshDistribution,
        min_length=LENGTH,
        max_length=LENGTH,
    )
    panel_densities = AsContainerOf(
        container_type=tuple,
        item_type=int | float,
        min_length=LENGTH,
        max_length=LENGTH,
    )
    lengths = AsContainerOf(
        container_type=tuple, item_type=float, min_length=LENGTH, max_length=LENGTH
    )

    def __init__(
        self,
        entity: Surface,
        mesh_distributions: tuple[MeshDistribution],
        panel_densities: tuple[int | float],
        lengths: tuple[float],
    ) -> Self:
        self.entity = entity
        self.mesh_distributions = mesh_distributions
        self.panel_densities = panel_densities
        self.lengths = lengths

    def foo():
        """Generates mesh points using"""


s = MeshGenerator(
    entity=BilinearSurface(
        Point(0, 0, 0), Point(1, 0, 0), Point(1, 1, 0), Point(0, 1, 0)
    ),
    mesh_distributions=(LinearDistribution(), LinearDistribution()),
    panel_densities=(3, 4.0),
    lengths=(20.0, 10.0),
)
print(s)
