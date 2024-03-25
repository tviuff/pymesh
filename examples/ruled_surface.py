"""Ruled surface example"""

import sys, os

sys.path.append(os.path.abspath(os.path.join("..", "pygdf")))

from pygdf import Point, Line, RuledSurface
from pygdf import LinearDistribution, ExponentialDistribution
from pygdf import GDFViewer

line_1 = Line(Point(0, 0, 0), Point(1, 0, 0))
line_2 = Line(Point(0, 1, 0), Point(1, 1, 0))

surface = RuledSurface(curve_1=line_1, curve_2=line_2)
surface.mesher.panel_densities = (0.2, 4)
surface.mesher.mesh_distributions = (
    LinearDistribution(),
    ExponentialDistribution(flip_direction=False),
)

surface_selection = RuledSurface.get_all_surfaces()

viewer = GDFViewer()
viewer.add_panels(surface_selection)
viewer.show()
