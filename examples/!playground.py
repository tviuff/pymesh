"""Rectangular surface example"""

import sys, os
sys.path.append(os.path.abspath(os.path.join('..', 'gdfgen')))

from gdfgen import mesh
from gdfgen.curves import Curve
from gdfgen import constants as const
from gdfgen import Line

print(isinstance(mesh.DistLinear(), mesh.DistMethod))
print(const.MeshConstants.DEFAULT_DIST_METHOD)
print(const.MeshConstants.DEFAULT_DIST_METHOD.name)
print(const.MeshConstants.DEFAULT_DIST_METHOD.value)
