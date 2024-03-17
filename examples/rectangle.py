"""Rectangular surface example"""

import sys, os
sys.path.append(os.path.abspath(os.path.join('..', 'gdf')))

from import Point, Line, CoonsPatch, GDFViewer

point1 = Point(0, 0, 0)
point2 = Point.set_relative_to(point1, dx=1.0)
point3 = Point(1, 1, 0)
point4 = Point(0, 1, 0)

line1 = Line(point1, point2)
line2 = Line(point2, point3)
line3 = Line(point3, point4)
line4 = Line(point4, point1)

surface1 = CoonsPatch(line1, line3, line2, line4)
for curve in surface1.curve_selection:
    print(curve)
surface1.num_points_u = 3
surface1.num_points_w = 3

viewer = GDFViewer(panel_normal_length=0.5)
viewer.add_panels(surface1,
    restricted_panels = [],
    include_vertex_annotation = False,
    include_normals = True
    )
viewer.show()
