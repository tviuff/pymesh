"""code playground"""

import sys, os
sys.path.append(os.path.abspath(os.path.join('..', 'gdfgen')))

from gdfgen import Point, Line, Arc3P, LinearlySweptSurface, GDFWriter
import plotting as plt

line = Line(Point(0, 0, 0), Point(0, 0, 1))
curve = Arc3P(Point(0, 0, 0), Point(1, 0, 0), Point(1, 0.0001, 0))
curve.flipped_dir = True
surface = LinearlySweptSurface(curve, line)
surface.num_points_curve = 30

surface_selection = surface

writer = GDFWriter()
writer.write(surface, "C:\\Users\\Flemming2\\Desktop\\test.gdf")
# plt.plot_mesh_points(surface_selection, xlim=(-1, 1), ylim=(-1, 1), zlim=(-1, 1))
