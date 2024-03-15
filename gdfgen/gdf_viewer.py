"""Module containing gdf viewer class"""

import numpy as np
from numpy import ndarray

from matplotlib import pyplot as plt
from matplotlib import style as mpl_style
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

from gdfgen.surfaces import Surface

class GDFViewer():
    """Plots surface panels and normals using matplotlib with the seaborn-v0_8 style"""

    def __init__(self) -> None:
        plt.close("all")
        mpl_style.use('seaborn-v0_8')
        ax = plt.figure().add_subplot(projection='3d')
        ax.set_xlabel('x')
        ax.set_ylabel('y')
        ax.set_zlabel('z')
        self._ax = ax
        self.xyzlim = np.array([0, 0, 0])

    @property
    def xyzlim(self) -> ndarray:
        return self._xyzlim

    @xyzlim.setter
    def xyzlim(self, value:ndarray):
        if not isinstance(value, ndarray):
            raise TypeError("xyzlim must be of type 'ndarray'")
        self._xyzlim = np.ceil(value)

    def __update_axis_limits(self, xyz):
        if isinstance(xyz, list):
            # panel vert
            xyzlim = np.max(np.abs(xyz), axis=0)
            self.xyzlim = np.max([self.xyzlim, xyzlim], axis=0)
        elif isinstance(xyz, ndarray):
            if len(xyz.shape) == 3:
                # mesh points
                x = np.max(np.abs(xyz[0, :, :]))
                y = np.max(np.abs(xyz[1, :, :]))
                z = np.max(np.abs(xyz[2, :, :]))
                xyzlim = np.array([x, y, z])
                self.xyzlim = np.max([self.xyzlim, xyzlim], axis=0)
            elif len(xyz.shape) == 2:
                #curve points
                xyzlim = np.max(np.abs(xyz), axis=0)
                self.xyzlim = np.max([self.xyzlim, xyzlim], axis=0)
            else:
                raise ValueError()
        else:
            raise ValueError()

    def __validate_surface_selection(self, selection) -> None:
        if not isinstance(selection, (tuple, list, Surface)):
            raise TypeError("selection must be of type 'Surface' or a tuple or list of such")
        if isinstance(selection, (list, tuple)):
            for item in selection:
                if not isinstance(item, Surface):
                    raise TypeError(
                        f"selection {type(selection).__name__} must contain items of type 'Surface'"
                    )

    def __organize_surface_selection(self, selection) -> tuple[Surface]:
        if isinstance(selection, list):
            return tuple(selection)
        if isinstance(selection, Surface):
            return (selection, )
        return selection

    def add_curve_points(self, xyz:ndarray) -> None:
        """Adds curve xyz points to plot"""
        ax = self._ax
        ax.scatter(xyz[:, 0], xyz[:, 1], xyz[:, 2], color='blue')
        self.__update_axis_limits(xyz)

    def add_mesh_points(self, surfaces) -> None:
        self.__validate_surface_selection(surfaces)
        surfaces = self.__organize_surface_selection(surfaces)
        ax = self._ax
        if isinstance(surfaces, Surface):
            xyz = surfaces.mesh_points
            self.__update_axis_limits(xyz)
            for i in range(0, xyz.shape[1]):
                for j in range(0, xyz.shape[2]):
                    ax.scatter(xyz[0,i,j], xyz[1,i,j], xyz[2,i,j], color='blue')
        else:
            for surface in surfaces:
                xyz = surface.mesh_points
                self.__update_axis_limits(xyz)
                for i in range(0, xyz.shape[1]):
                    for j in range(0, xyz.shape[2]):
                        ax.scatter(xyz[0,i,j], xyz[1,i,j], xyz[2,i,j], color='blue')

    def add_panels(self, surfaces) -> None:
        self.__validate_surface_selection(surfaces)
        surfaces = self.__organize_surface_selection(surfaces)
        ax = self._ax
        if isinstance(surfaces, Surface):
            for panel in surfaces.panels:
                x, y, z = panel[0::3], panel[1::3], panel[2::3]
                verts = [list(zip(x, y, z))]
                for xyz in verts:
                    self.__update_axis_limits(xyz)
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
                    for xyz in verts:
                        self.__update_axis_limits(xyz)
                    ax.add_collection3d(Poly3DCollection(
                        verts,
                        facecolors = '#0072BD',
                        linewidths = .5,
                        edgecolors = 'black',
                        alpha = .8
                    ))

    def _plot_normals(self, panel:ndarray) -> None:
        pass

    def show(self):
        ax = self._ax
        xlim = (-np.ceil(self.xyzlim[0]), np.ceil(self.xyzlim[0]))
        ylim = (-np.ceil(self.xyzlim[1]), np.ceil(self.xyzlim[1]))
        zlim = (-np.ceil(self.xyzlim[2]), np.ceil(self.xyzlim[2]))
        ax.set(xlim=xlim)
        ax.set(ylim=ylim)
        ax.set(zlim=zlim)
        plt.show()
