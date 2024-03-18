"""Ruled surface example"""

import sys, os
sys.path.append(os.path.abspath(os.path.join('..', 'gdf')))

from gdf import Point, Line, RuledSurface, GDFViewer

line1 = Line(Point(0, 0, 0), Point(0, 1, 0))
line2 = Line(Point(1, 0, 0), Point(1, 1, 0))

surface = RuledSurface(curve1=line1, curve2=line2)
surface.num_points_u = 3
surface.num_points_w = 3

viewer = GDFViewer()
viewer.add_panels(surface, include_normals=True, include_vertex_annotation=True)
viewer.show()
