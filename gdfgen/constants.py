"""Module with project constants
"""

from enum import Enum

from gdfgen import mesh

class MeshConstants(Enum):
    """Contains mesh constants"""

    DEFAULT_NUM_POINT = 5
    DEFAULT_DIST_METHOD = mesh.DistLinear() # use () ath the end to instanciate the class !
