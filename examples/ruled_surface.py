"""Ruled surface example"""

import sys, os

sys.path.append(os.path.abspath(os.path.join("..", "pygdf")))

from pymesh import Point, Line, RuledSurface
from pymesh import ExponentialDistribution
from pymesh import MeshViewer

line1 = Line(Point(0, 0, 0), Point(1, 0, 0))
line2 = Line(Point(0, 1, 0), Point(1, 1, 0))

surface = RuledSurface(curve1=line1, curve2=line2)
surface.mesher.set_u_parameters(panel_density=0.2)
surface.mesher.set_w_parameters(panel_density=4, distribution=ExponentialDistribution())

surface_copy = surface.copy()
surface_copy.move(dx=-1, dy=-1)

surface_selection = RuledSurface.get_all_surfaces()

viewer = MeshViewer()
viewer.add_panels(surface_selection)
viewer.show()
