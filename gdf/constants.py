"""Module with project constants
"""

from enum import Enum

from gdf.mesh.distribution_methods import DistLinear

class MeshConstants(Enum):
    """Contains mesh constants"""

    DEFAULT_NUM_POINT = 5
    DEFAULT_DIST_METHOD = DistLinear() # use class instance!
