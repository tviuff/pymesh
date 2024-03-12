"""Main module for trying out code ideas
"""

import time

from matplotlib import pyplot as plt
from matplotlib import style as mpl_style
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

import gdfgen as gdf

# ? Modify CoonsPatch.set_dist_methods(u_dists=[u0, u1], w_dists=[0w, 1w]) ?

def main():
    """Function executed if file is executed and not imported"""

    # surface_selection, azim, elev = example_rectangle_xy()
    surface_selection, azim, elev = example_circle()
    
    # plot_points(surface_selection, azim, elev)
    plot_panels(surface_selection, azim, elev, 3)

def time_it(func):
    """Wrapper function used to time function execution time"""
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print(f"Exceution of '{func.__name__}' took {round((end - start) * 1000)} mil sec.")
        return result
    return wrapper

def plot_points(surface_sellection:tuple, azim:int=None, elev:int=None):
    """Plots mesh xyz points of surfaces in surface_selection"""

    mpl_style.use('seaborn-v0_8')
    plt.close("all")
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

def plot_panels(surface_sellection:tuple, azim:int=None, elev:int=None, box_lim:float|int=None):
    """Plots surfaces panels of surface_selection"""

    mpl_style.use('seaborn-v0_8')
    plt.close("all")
    fig = plt.figure()
    ax = fig.add_subplot(projection='3d')
    for surface in surface_sellection:
        for panel in surface.panels:
            x, y, z = panel[0::3], panel[1::3], panel[2::3]
            verts = [list(zip(x, y, z))]
            ax.add_collection3d(Poly3DCollection(
                verts,
                facecolors = '#0072BD',
                linewidths = .5,
                edgecolors = 'black',
                alpha = .8
            ))
    if box_lim is not None:
        ax.set(
            xlim = (-box_lim, box_lim),
            ylim = (-box_lim, box_lim),
            zlim = (-box_lim, box_lim)
        )
    ax.set_xlabel('x (m)')
    ax.set_ylabel('y (m)')
    ax.set_zlabel('z (m)')
    ax.view_init(azim=azim, elev=elev)
    plt.show()

@time_it
def example_rectangle_xy():
    """Rectangular surface example"""

    point1 = gdf.Point(0, 0, 0)
    point2 = gdf.Point.set_relative_to(point1, dx=1.0)
    point3 = gdf.Point(1, 1, 0)
    point4 = gdf.Point(0, 1, 0)

    line1 = gdf.Line(point1, point2)
    line2 = gdf.Line(point2, point3)
    line3 = gdf.Line(point3, point4)
    line4 = gdf.Line(point4, point1)

    surface1 = gdf.CoonsPatch(line1, line3, line2, line4)
    surface1.set_num_points(num_points_u=10, num_points_w=10)
    
    surface_selection = (surface1,)

    return surface_selection, 270, 90

@time_it
def example_circle():
    """Circle surface example"""

    point_ctr = gdf.Point(0, 0, 0)
    point_bl = gdf.Point(-1, -1, 0)
    point_br = gdf.Point.set_relative_to(point_bl, dx=2.0)
    point_tl = gdf.Point(-1, 1, 0)
    point_tr = gdf.Point(+1, 1, 0)

    # Rectangle in centre
    line1 = gdf.Line(point_bl, point_br)
    line2 = gdf.Line(point_tl, point_tr)
    line3 = gdf.Line(point_bl, point_tl)
    line4 = gdf.Line(point_br, point_tr)
    surface1 = gdf.CoonsPatch(line1, line2, line3, line4)

    point_bl_ext = gdf.Point.set_relative_to(point_bl, dx=-1.0, dy=-1.0)
    point_br_ext = gdf.Point.set_relative_to(point_br, dx=+1.0, dy=-1.0)
    point_tl_ext = gdf.Point.set_relative_to(point_tl, dx=-1.0, dy=+1.0)
    point_tr_ext = gdf.Point.set_relative_to(point_tr, dx=+1.0, dy=+1.0)

    # Bottom semi-circle
    line5 = gdf.Line(point_bl_ext, point_bl)
    line6 = gdf.Line(point_br_ext, point_br)
    line7 = gdf.Arc3(point_ctr, point_bl_ext, point_br_ext)
    surface2 = gdf.CoonsPatch(line7, line1, line5, line6)
    surface2.set_num_points(8, 8)
    # surface2.set_dist_methods(dist_0w=gdf.mesh.DistCosineEnd1, dist_1w=gdf.mesh.DistCosineEnd1)

    # Top semi-circle
    line8 = gdf.Line(point_tl, point_tl_ext)
    line9 = gdf.Line(point_tr, point_tr_ext)
    line10 = gdf.Arc3(point_ctr, point_tl_ext, point_tr_ext)
    surface3 = gdf.CoonsPatch(line2, line10, line8, line9)

    # Left semi-circle
    line12 = gdf.Arc3(point_ctr, point_tl_ext, point_bl_ext)
    surface4 = gdf.CoonsPatch(line3, line8, line12, line5)

    # Right semi-circle
    line13 = gdf.Arc3(point_ctr, point_tr_ext, point_br_ext)
    surface5 = gdf.CoonsPatch(line4, line6, line13, line9)

    surface_selection = (surface1, surface2, surface3, surface4, surface5)
    
    return surface_selection, 270, 90

if __name__ == "__main__":
    main()
