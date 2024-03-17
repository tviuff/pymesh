"""code playground"""

import sys, os
sys.path.append(os.path.abspath(os.path.join('..', 'gdf')))

from gdf import Point, Line, Arc3P, SweptSurface, GDFViewer

line = Line(Point(0, 0, 0), Point(0, 0, 1))
curve = Arc3P(Point(0, 0, 0), Point(1, 0, 0), Point(1, 0.0001, 0))
curve.flipped_dir = True
surface = SweptSurface(curve, line)
surface.num_points_curve = 30
surface.flip_normal = True

surface_selection = surface

viewer = GDFViewer(panel_normal_length=0.25)
viewer.add_panels(surface_selection, include_normals=True)
viewer.show()
