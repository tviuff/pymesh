
"""Module containing plot functions for plotting example file results"""

from numpy import ndarray

from matplotlib import pyplot as plt
from matplotlib import style as mpl_style
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

from gdfgen.surfaces import Surface

def set_xyz_lim(
        ax,
        xlim:tuple[float] = None,
        ylim:tuple[float] = None,
        zlim:tuple[float] = None
    ):
    if xlim is not None:
        ax.set(xlim=xlim)
    if ylim is not None:
        ax.set(ylim=ylim)
    if zlim is not None:
        ax.set(zlim=zlim)

def plot_curve_points(
        xyz:ndarray,
        azim:int=None,
        elev:int=None,
        xlim:tuple[float]=None,
        ylim:tuple[float]=None,
        zlim:tuple[float]=None
    ):
    """Plots curve xyz points"""

    plt.close("all")
    mpl_style.use('seaborn-v0_8')
    fig = plt.figure()
    ax = fig.add_subplot(projection='3d')
    ax.scatter(xyz[:, 0], xyz[:, 1], xyz[:, 2], color='blue')
    set_xyz_lim(ax, xlim, ylim, zlim)
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.set_zlabel('z')
    ax.view_init(azim=azim, elev=elev)
    plt.show()

def plot_mesh_points(
        surfaces:tuple[Surface]|list[Surface]|Surface,
        azim:int=None,
        elev:int=None,
        xlim:tuple[float]=None,
        ylim:tuple[float]=None,
        zlim:tuple[float]=None
        ):
    """Plots mesh xyz points of surfaces in surface_selection"""

    if not isinstance(surfaces, (list, tuple, Surface)):
        raise TypeError("Surfaces must be either a single surface or a list/tuple of surfaces")
    
    mpl_style.use('seaborn-v0_8')
    plt.close("all")
    fig = plt.figure()
    ax = fig.add_subplot(projection='3d')

    if isinstance(surfaces, Surface):
        xyz = surfaces.mesh_points
        for i in range(0, xyz.shape[1]):
            for j in range(0, xyz.shape[2]):
                ax.scatter(xyz[0,i,j], xyz[1,i,j], xyz[2,i,j], color='blue')
    else:
        for surface in surfaces:
            xyz = surface.mesh_points
            for i in range(0, xyz.shape[1]):
                for j in range(0, xyz.shape[2]):
                    ax.scatter(xyz[0,i,j], xyz[1,i,j], xyz[2,i,j], color='blue')

    set_xyz_lim(ax, xlim, ylim, zlim)
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.set_zlabel('z')
    ax.view_init(azim=azim, elev=elev)
    plt.show()

def plot_panels(
        surfaces:tuple[Surface]|list[Surface]|Surface,
        azim:int = None,
        elev:int = None,
        xlim:tuple[float]=None,
        ylim:tuple[float]=None,
        zlim:tuple[float]=None
    ):
    """Plots surfaces panels of surface_selection"""

    if not isinstance(surfaces, (list, tuple, Surface)):
        raise TypeError("Surfaces must be either a single surface or a list/tuple of surfaces")

    mpl_style.use('seaborn-v0_8')
    plt.close("all")
    fig = plt.figure()
    ax = fig.add_subplot(projection='3d')

    if isinstance(surfaces, Surface):
        for panel in surfaces.panels:
            x, y, z = panel[0::3], panel[1::3], panel[2::3]
            verts = [list(zip(x, y, z))]
            ax.add_collection3d(Poly3DCollection(
                verts,
                facecolors = '#0072BD',
                linewidths = .5,
                edgecolors = 'black',
                alpha = .8
            ))
    else:
        for surface in surfaces:
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
    set_xyz_lim(ax, xlim, ylim, zlim)
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.set_zlabel('z')
    ax.view_init(azim=azim, elev=elev)
    plt.show()