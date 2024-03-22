"""Module with project constants
"""

from enum import Enum

from gdf.mesh.distribution_methods import LinearDistribution

class MeshConstants(Enum):
    """Contains mesh constants"""

    DEFAULT_NUM_POINT = 5
    DEFAULT_DENSITY = 0.2
    DEFAULT_DIST_METHOD = LinearDistribution
