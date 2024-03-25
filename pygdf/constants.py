"""Module with project constants
"""

from enum import Enum

from pygdf.mesh.distribution_types import LinearDistribution


class MeshConstants(Enum):
    """Contains mesh constants"""

    DEFAULT_DENSITY = 0.5
    DEFAULT_DISTRIBUTION_METHOD = LinearDistribution
