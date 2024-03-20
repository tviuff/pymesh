"""Bilinear surface example"""

import sys, os
sys.path.append(os.path.abspath(os.path.join('..', 'gdf')))

from gdf import Point, BilinearSurface, DistLinear, GDFViewer

point1 = Point(0, 0, 0)
point2 = Point(1, 0, 0)
point3 = Point(1, 1, 0)
point4 = Point(0, 1, -1)

surface = BilinearSurface(point00=point1, point01=point2, point10=point4, point11=point3)
surface.num_points_01 = 10
surface.num_points_02 = 10
surface.dist_01 = DistLinear()

surface_selection = BilinearSurface.get_all_surfaces()

viewer = GDFViewer()
viewer.add_panels(surface_selection)
viewer.show()
