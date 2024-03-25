"""Swept surface example"""

import sys, os

sys.path.append(os.path.abspath(os.path.join("..", "pygdf")))

from pymesh import Point, Line, Arc3P, SweptSurface
from pymesh import LinearDistribution, CosineDistribution
from pymesh import GDFViewer

line = Line(Point(0, 0, 0), Point(0, 0, 1))
curve = Arc3P(Point(0, 0, 0), Point(1, 0, 0), Point(0, 1, 0))
curve.invert_arc = True

surface = SweptSurface(curve=curve, sweeper_curve=line)
surface.mesher.panel_densities = (0.2, 3)
surface.mesher.mesh_distributions = (
    LinearDistribution(),
    CosineDistribution(flip_direction=False),
)

surface_selection = SweptSurface.get_all_surfaces()

viewer = GDFViewer()
viewer.add_panels(surface_selection)
viewer.show()
