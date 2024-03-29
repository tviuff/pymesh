"""Bilinear surface example"""

import sys, os

sys.path.append(os.path.abspath(os.path.join("..", "pymesh")))

from pymesh import Point, BilinearSurface
from pymesh import LinearDistribution, ExponentialDistribution
from pymesh import MeshViewer

point00 = Point(0, 0, 0)
point10 = Point(1, 0, -1)
point11 = Point(1, 1, 0)
point01 = Point(0, 1, 0)

surface = BilinearSurface(point00, point10, point11, point01)

surface.mesher.set_u_parameters(5, LinearDistribution())
surface.mesher.set_w_parameters(10, ExponentialDistribution())

surface_copy = surface.copy(deepcopy=True)
surface_copy.move(dx=-1, dy=-1)

surface_selection = BilinearSurface.get_all_surfaces()

viewer = MeshViewer()
viewer.add_panels(surface_selection)
viewer.show()
