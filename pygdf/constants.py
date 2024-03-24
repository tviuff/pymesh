"""Module with project constants
"""

from enum import Enum

from pygdf.mesh_distributions import LinearDistribution

class MeshConstants(Enum):
    """Contains mesh constants"""

    DEFAULT_DENSITY = 0.5
    DEFAULT_DIST_METHOD = LinearDistribution
