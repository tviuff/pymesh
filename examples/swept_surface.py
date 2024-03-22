"""Swept surface example"""

import sys, os
sys.path.append(os.path.abspath(os.path.join('..', 'gdf')))

from gdf import Point, Line, Arc3P, SweptSurface, CosineDistribution, GDFViewer

line = Line(Point(0, 0, 0), Point(0, 0, 1))
curve = Arc3P(Point(0, 0, 0), Point(1, 0, 0), Point(0, 1, 0))
curve.invert_arc = True

surface = SweptSurface(curve=curve, sweeper_curve=line)
surface.panel_density_curve = .2
surface.panel_density_sweeper_curve = 3
surface.boundary_distribution_sweeper_curve = CosineDistribution(flip_direction=False)

surface_selection = SweptSurface.get_all_surfaces()

viewer = GDFViewer()
viewer.add_panels(surface_selection)
viewer.show()
