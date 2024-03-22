"""Swept surface example"""

import sys, os
sys.path.append(os.path.abspath(os.path.join('..', 'gdf')))

from gdf import Point, Line, Arc3P, SweptSurface, GDFViewer

line = Line(Point(0, 0, 0), Point(0, 0, 1))
curve = Arc3P(Point(0, 0, 0), Point(1, 0, 0), Point(1, 0.0001, 0))
curve.invert_arc = True
surface = SweptSurface(curve=curve, sweeper_curve=line)
surface.num_points_curve = 50

surface_selection = SweptSurface.get_all_surfaces()

viewer = GDFViewer()
viewer.add_panels(surface_selection)
viewer.show()
