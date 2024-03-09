"""Main module for trying out code ideas
"""

import time

from matplotlib import pyplot as plt

import gdfgen as gdf

def main():
    """Function executed if file is executed and not imported"""

    # ! Modify CoonsPatch._validate_curve_selection() to check if curves share points
    # ! and set self.curve_u0, self.curve_u1, etc.
    # ! Flip mesh direction by multiplying with 1 - dist_fn(u)
    # ! Modify CoonsPatch.set_dist_methods(u_dists=[u0, u1], w_dists=[0w, 1w])

    surface_selection, azim, elev = example_vertical_cylinder()
    plot_points(surface_selection, azim, elev)

def time_it(func):
    """Wrapper function used to time function execution time"""
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print(f"{func.__name__} took {round((end - start) * 1000)} mil sec")
        return result
    return wrapper

@time_it
def plot_points(surface_sellection:tuple, azim=None, elev=None):
    """Plots mesh xyz points of surfaces in surface_selection"""

    plt.close("all")
    plt.style.use('dark_background')
    fig = plt.figure()
    ax = fig.add_subplot(projection='3d')
    for surface in surface_sellection:
        xyz = surface.mesh_points
        for i in range(0, xyz.shape[1]):
            for j in range(0, xyz.shape[2]):
                ax.scatter(xyz[0,i,j], xyz[1,i,j], xyz[2,i,j], color='blue')
    ax.set_xlabel('x (m)')
    ax.set_ylabel('y (m)')
    ax.set_zlabel('z (m)')
    ax.view_init(azim=azim, elev=elev)
    plt.show()

def example_rectangle_xy():
    """Rectangular surface example"""

    point_bl = gdf.Point(0, 0, 0)
    point_br = gdf.Point.set_relative_to(point_bl, dx=1.0)
    point_tr = gdf.Point(1, 1, 0)
    point_tl = gdf.Point(0, 1, 0)

    line1 = gdf.Line(point_bl, point_br)
    line2 = gdf.Line(point_tl, point_tr)
    line3 = gdf.Line(point_bl, point_tl)
    line4 = gdf.Line(point_br, point_tr)

    surface1 = gdf.CoonsPatch(line1, line2, line3, line4)
    surface1.set_num_points(num_points_u=10, num_points_w=10)

    surface_selection = (surface1,)

    return surface_selection, 270, 90

def example_vertical_cylinder():
    """Vertical cylinder surface example"""

    point_ctr = gdf.Point(0, 0, 0)
    point_bl = gdf.Point(-1, -1, 0)
    point_br = gdf.Point.set_relative_to(point_bl, dx=2.0)
    point_tl = gdf.Point(-1, 1, 0)
    point_tr = gdf.Point(+1, 1, 0)

    line1 = gdf.Line(point_bl, point_br)
    line2 = gdf.Line(point_tl, point_tr)
    line3 = gdf.Line(point_bl, point_tl)
    line4 = gdf.Line(point_br, point_tr)
    surface1 = gdf.CoonsPatch(line1, line2, line3, line4)

    point_bl_ext = gdf.Point.set_relative_to(point_bl, dx=-1.0, dy=-1.0)
    point_br_ext = gdf.Point.set_relative_to(point_br, dx=+1.0, dy=-1.0)
    point_tl_ext = gdf.Point.set_relative_to(point_tl, dx=-1.0, dy=+1.0)
    point_tr_ext = gdf.Point.set_relative_to(point_tr, dx=+1.0, dy=+1.0)

    line5 = gdf.Line(point_bl_ext, point_bl)
    line6 = gdf.Line(point_br_ext, point_br)
    line7 = gdf.Arc3(point_ctr, point_bl_ext, point_br_ext)
    surface2 = gdf.CoonsPatch(line7, line1, line5, line6)

    line8 = gdf.Line(point_tl, point_tl_ext)
    line9 = gdf.Line(point_tr, point_tr_ext)
    line10 = gdf.Arc3(point_ctr, point_tl_ext, point_tr_ext)
    surface3 = gdf.CoonsPatch(line2, line10, line8, line9)

    surface_selection = (surface1, surface2, surface3)

    return surface_selection, 270, 90

if __name__ == "__main__":
    main()
