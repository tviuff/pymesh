"""Module with project constants
"""

from enum import Enum

from pymesh.mesh.distributions import LinearDistribution


class MeshConstants(Enum):
    """Contains mesh constants"""

    DEFAULT_DENSITY = 0.5
    DEFAULT_DISTRIBUTION_METHOD = LinearDistribution
