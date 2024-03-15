"""Circle panel example"""

import sys, os
sys.path.append(os.path.abspath(os.path.join('..', 'gdfgen')))

from gdfpy import mesh, Point, Line, Arc3P, CoonsPatch, GDFViewer

# Points forming an inner rectangle in the circle
point_ctr = Point(0, 0, 0)
point_bl = Point(-1, -1, 0)
point_br = Point.set_relative_to(point_bl, dx=2.0)
point_tl = Point(-1, 1, 0)
point_tr = Point(+1, 1, 0)

# Lines connecting above points to form a rectangle
line1 = Line(point_bl, point_br)
line2 = Line(point_tl, point_tr)
line3 = Line(point_bl, point_tl)
line4 = Line(point_br, point_tr)
surface1 = CoonsPatch(line1, line2, line3, line4)

# Points on the periferi of the circe
point_bl_ext = Point.set_relative_to(point_bl, dx=-1.0, dy=-1.0)
point_br_ext = Point.set_relative_to(point_br, dx=+1.0, dy=-1.0)
point_tl_ext = Point.set_relative_to(point_tl, dx=-1.0, dy=+1.0)
point_tr_ext = Point.set_relative_to(point_tr, dx=+1.0, dy=+1.0)

# Bottom semi-circle and surface patch
line5 = Line(point_bl_ext, point_bl)
line6 = Line(point_br_ext, point_br)
line7 = Arc3P(point_ctr, point_bl_ext, point_br_ext)
surface2 = CoonsPatch(line7, line1, line5, line6)
surface2.num_points_u = 5
surface2.num_points_w = 5
surface2.dist_0w = mesh.DistLinear()
surface2.dist_1w = mesh.DistLinear()

# Top semi-circle and surface patch
line8 = Line(point_tl, point_tl_ext)
line9 = Line(point_tr, point_tr_ext)
line10 = Arc3P(point_ctr, point_tl_ext, point_tr_ext)
surface3 = CoonsPatch(line2, line10, line8, line9)

# Left semi-circle and surface patch
line12 = Arc3P(point_ctr, point_tl_ext, point_bl_ext)
surface4 = CoonsPatch(line3, line8, line12, line5)

# Right semi-circle and surface patch
line13 = Arc3P(point_ctr, point_tr_ext, point_br_ext)
surface5 = CoonsPatch(line4, line6, line13, line9)

surface_selection = (surface1, surface2, surface3, surface4, surface5)

viewer = GDFViewer()
viewer.add_panels(surface_selection)
viewer.show()
