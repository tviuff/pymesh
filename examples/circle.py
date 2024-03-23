"""Circle panel example"""

import sys, os

sys.path.append(os.path.abspath(os.path.join('..', 'gdf')))

from gdf import Point, Line, Arc3P, CoonsPatch, LinearDistribution, GDFViewer

# Points forming an inner rectangle in the circle
point_ctr = Point(0, 0, 0)
point_bl = Point(-1, -1, 0)
point_br = point_bl.create_relative_point(dx=2.0)
point_tl = Point(-1, 1, 0)
point_tr = Point(+1, 1, 0)

# Lines connecting above points to form a rectangle
line1 = Line(point_bl, point_br)
line2 = Line(point_tl, point_tr)
line3 = Line(point_bl, point_tl)
line4 = Line(point_br, point_tr)
surface1 = CoonsPatch([line1, line2, line3, line4])
surface1.flip_panel_normals()

# Points on the periferi of the circe
point_bl_ext = point_bl.create_relative_point(dx=-1.0, dy=-1.0)
point_br_ext = point_br.create_relative_point(dx=+1.0, dy=-1.0)
point_tl_ext = point_tl.create_relative_point(dx=-1.0, dy=+1.0)
point_tr_ext = point_tr.create_relative_point(dx=+1.0, dy=+1.0)

# Bottom semi-circle and surface patch
line5 = Line(point_bl_ext, point_bl)
line6 = Line(point_br_ext, point_br)
line7 = Arc3P(point_ctr, point_bl_ext, point_br_ext)
surface2 = CoonsPatch([line7, line1, line5, line6])
surface2.panel_density_u = 7
surface2.panel_density_w = 2
surface2.boundary_distribution_w = LinearDistribution()
surface2.flip_panel_normals()

# Top semi-circle and surface patch
line8 = Line(point_tl, point_tl_ext)
line9 = Line(point_tr, point_tr_ext)
line10 = Arc3P(point_ctr, point_tl_ext, point_tr_ext)
surface3 = CoonsPatch([line2, line10, line8, line9])
surface3.flip_panel_normals()

# Left semi-circle and surface patch
line12 = Arc3P(point_ctr, point_tl_ext, point_bl_ext)
surface4 = CoonsPatch([line3, line8, line12, line5])
surface4.flip_panel_normals()

# Right semi-circle and surface patch
line13 = Arc3P(point_ctr, point_tr_ext, point_br_ext)
surface5 = CoonsPatch([line4, line6, line13, line9])

surface_selection = CoonsPatch.get_all_surfaces()

if __name__ == "__main__":
    viewer = GDFViewer(panel_normal_length=0.5)
    viewer.add_panels(
        surfaces = surface_selection,
        include_normals = True
        )
    viewer.show()
