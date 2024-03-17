"""Module with project constants
"""

from enum import Enum

from gdf import mesh

class MeshConstants(Enum):
    """Contains mesh constants"""

    DEFAULT_NUM_POINT = 5
    DEFAULT_DIST_METHOD = mesh.DistLinear() # use class instance!
