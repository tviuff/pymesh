"""Rectangular surface example"""

import sys, os
sys.path.append(os.path.abspath(os.path.join('..', 'gdfgen')))

from gdfpy import Point, PlaneSurface, GDFViewer

point1 = Point(0, 0, 0)
point2 = Point(1, 0, 0)
point3 = Point(0, 1, 0)

surface = PlaneSurface(point0=point1, point1=point2, point2=point3)
surface.num_points_01 = 3
surface.num_points_02 = 5

viewer = GDFViewer()
viewer.add_panels(surface, include_normals=True)
viewer.show()
