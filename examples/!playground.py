"""code playground"""

import sys, os

sys.path.append(os.path.abspath(os.path.join("..", "pymesh")))

from pymesh import Point, Line, Arc3P, SweptSurface
from pymesh import ExponentialDistribution
from pymesh import MeshGenerator, MeshViewer


line = Line(Point(0, 0, 0), Point(0, 0, 1))
curve = Arc3P(Point(0, 0, 0), Point(1, 0, 0), Point(1, 0.0001, 0))
curve.inverse_sector = True

surface1 = SweptSurface(curve, line)
surface1.flip_normal()

line2 = Line(Point(0, 0, 1), Point(0, 1, 1))
line3 = Line(Point(0, 0, 1), Point(1, 1, 1))
surface2 = SweptSurface(line2, line3)
surface2.flip_normal()

mesher = MeshGenerator()
mesher.add_surface(surface1)
mesher.add_surface(surface2, distribution_u=ExponentialDistribution())

viewer = MeshViewer(mesher, panel_normal_length=0.25)
viewer.show()
