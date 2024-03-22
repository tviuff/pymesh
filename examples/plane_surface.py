"""Rectangular surface example"""

import sys, os
sys.path.append(os.path.abspath(os.path.join('..', 'gdf')))

from gdf import Point, PlaneSurface, LinearDistribution, CosineDistribution, GDFViewer

point_0 = Point(0, 0, 0)
point_1 = Point(1, 0, 0)
point_2 = Point(0, 1, 0)

surface = PlaneSurface(point_0=point_0, point_1=point_1, point_2=point_2)
surface.panel_density_01 = .2
surface.panel_density_02 = .2
surface.boundary_distribution_01 = LinearDistribution()
surface.boundary_distribution_02 = CosineDistribution(flip_direction=True)

surface_selection = PlaneSurface.get_all_surfaces()

viewer = GDFViewer()
viewer.add_panels(surface_selection, include_normals=True)
viewer.show()
