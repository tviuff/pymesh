"""Rectangular surface example"""

import sys, os
sys.path.append(os.path.abspath(os.path.join('..', 'gdf')))

from gdf import Point, PlaneSurface, GDFViewer

point1 = Point(0, 0, 0)
point2 = Point(1, 0, 0)
point3 = Point(0, 1, 0)

surface = PlaneSurface(point0=point1, point1=point2, point2=point3)
surface.num_points_01 = 3
surface.num_points_02 = 3

surface_selection = PlaneSurface.get_all_surfaces()

viewer = GDFViewer()
viewer.add_panels(surface_selection, include_normals=True)
viewer.show()
