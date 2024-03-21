"""Rectangular surface example"""

import sys, os
sys.path.append(os.path.abspath(os.path.join('..', 'gdf')))

from gdf import Point, Line, CoonsPatch, CosineDistribution, GDFViewer

point1 = Point(0, 0, 0)
point2 = point1.create_relative_point(dx=1.0)
point3 = Point(1, 1, 0)
point4 = Point(0, 1, 0)

line1 = Line(point1, point2)
line2 = Line(point2, point3)
line3 = Line(point3, point4)
line4 = Line(point4, point1)

surface1 = CoonsPatch([line1, line3, line2, line4])
for curve in surface1.curves:
    print(curve)
surface1.flip_normal = True
surface1.num_points_u = 5
surface1.num_points_w = 7
surface1.dist_u = CosineDistribution(flip_direction=True)

surface_selection = CoonsPatch.get_all_surfaces()

viewer = GDFViewer(panel_normal_length=0.5)
viewer.add_panels(surface_selection,
    restricted_panels = [],
    include_vertex_annotation = False,
    include_normals = True
    )
viewer.show()
