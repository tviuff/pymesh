"""Module with project constants
"""

from enum import Enum

from .mesh import DistributionMethod, Linear

class MeshConstants(Enum):
    """Contains mesh constants"""

    DEFAULT_NUM_POINT = 10
    DEFAULT_DIST_METHOD:DistributionMethod = Linear
