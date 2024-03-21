"""Rectangular surface example"""

import sys, os
sys.path.append(os.path.abspath(os.path.join('..', 'gdf')))

# examples/rectangle.py

from gdf import Point, Line, CoonsPatch, CosineDistribution, GDFViewer

point1 = Point(0, 0, 0)
point2 = Point(1, 0, 0)
point3 = Point(1, 1, 0)
point4 = Point(0, 1, 0)

line1 = Line(point1, point2)
line2 = Line(point2, point3)
line3 = Line(point3, point4)
line4 = Line(point4, point1)

surface = CoonsPatch([line1, line3, line2, line4])
surface.flip_normal = True # flips surface panel normals
surface.num_points_u = 5 # specifies number of points along the u dimension
surface.num_points_w = 7 # specifies number of points along the w dimension
surface.dist_u = CosineDistribution(flip_direction=True) # distribution method along the u dimension

surface_selection = CoonsPatch.get_all_surfaces()

viewer = GDFViewer(panel_normal_length=0.5) # specify panel normal length for visualization
viewer.add_panels(surface_selection, include_normals=True) # include panel normals
viewer.show() # plot the surface panels
