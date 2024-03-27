"""Module with project constants
"""

from enum import Enum

from pymesh.mesh.mesh_distributions import LinearDistribution


class MeshConstants(Enum):
    """Contains mesh constants"""

    DEFAULT_DENSITY = 0.2
    DEFAULT_DISTRIBUTION_METHOD = LinearDistribution
