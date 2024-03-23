"""Mdule containing utility functions
"""

import time

from gdf import Point, Line, Arc3P, CoonsPatch, LinearDistribution # ! IMPORT ABS PATH

def time_it(func):
    """Wrapper function used to time function execution time"""
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print(f"Exceution of '{func.__name__}' took {round((end - start) * 1000)} mil sec.")
        return result
    return wrapper

def circle_in_xy_plane(
        point_ctr = Point(0, 0, 0),
        radius = 1,
        ratio = 0.5,
    ):

    # Points forming an inner rectangle in the circle
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
    surface1.flip_normal = True

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
    surface2.dist_0w = LinearDistribution()
    surface2.dist_1w = LinearDistribution()
    surface2.flip_normal = True

    # Top semi-circle and surface patch
    line8 = Line(point_tl, point_tl_ext)
    line9 = Line(point_tr, point_tr_ext)
    line10 = Arc3P(point_ctr, point_tl_ext, point_tr_ext)
    surface3 = CoonsPatch(line2, line10, line8, line9)
    surface3.flip_normal = True

    # Left semi-circle and surface patch
    line12 = Arc3P(point_ctr, point_tl_ext, point_bl_ext)
    surface4 = CoonsPatch(line3, line8, line12, line5)
    surface4.flip_normal = True

    # Right semi-circle and surface patch
    line13 = Arc3P(point_ctr, point_tr_ext, point_br_ext)
    surface5 = CoonsPatch(line4, line6, line13, line9)

    return (surface1, surface2, surface3, surface4, surface5)
