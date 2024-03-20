"""Ruled surface example"""

import sys, os
sys.path.append(os.path.abspath(os.path.join('..', 'gdf')))

from gdf import Point, Line, RuledSurface, GDFViewer

line1 = Line(Point(0, 0, 0), Point(0, 1, 0))
line2 = Line(Point(1, 0, 0), Point(1, 1, 0))

surface = RuledSurface(curve1=line1, curve2=line2)
surface.num_points_1 = 3
surface.num_points_2 = 3

surface_selection = RuledSurface.get_all_surfaces()

viewer = GDFViewer()
viewer.add_panels(surface_selection, include_normals=True, include_vertex_annotation=True)
viewer.show()
