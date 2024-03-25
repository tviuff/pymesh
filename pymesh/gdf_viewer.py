"""Module containing gdf viewer class"""

import numpy as np

from matplotlib import pyplot as plt
from matplotlib import style as mpl_style
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

from pymesh.surfaces.surface import Surface

# ! fix typing of NDArray cases


class GDFViewer:
    """Plots surface panels and normals using matplotlib with seaborn-v0_8 style"""

    def __init__(self, panel_normal_length: float = 1.0) -> None:
        plt.close("all")
        mpl_style.use("seaborn-v0_8")
        fig = plt.figure()
        fig.patch.set_facecolor("#EAEAF2")
        ax = fig.add_subplot(projection="3d")
        ax.set_xlabel("X axis")
        ax.set_ylabel("Y axis")
        ax.set_zlabel("Z axis")
        self._panel_normal_length = panel_normal_length
        self._ax = ax
        self.xyzlim = np.array([1, 1, 1])

    def get_ax(self):
        return self._ax

    @property
    def panel_normal_length(self) -> float:
        return self._panel_normal_length

    @property
    def xyzlim(self) -> np.ndarray:
        return self._xyzlim

    @xyzlim.setter
    def xyzlim(self, value: np.ndarray):
        if not isinstance(value, np.ndarray):
            raise TypeError("xyzlim must be of type 'ndarray'")
        self._xyzlim = np.ceil(value)

    def __update_axis_limits(self, xyz):
        if isinstance(xyz, list):
            # panel vert
            xyzlim = np.max(np.abs(xyz), axis=0)
            self.xyzlim = np.max([self.xyzlim, xyzlim], axis=0)
        elif isinstance(xyz, np.ndarray):
            if len(xyz.shape) == 3:
                # mesh points
                x = np.max(np.abs(xyz[0, :, :]))
                y = np.max(np.abs(xyz[1, :, :]))
                z = np.max(np.abs(xyz[2, :, :]))
                xyzlim = np.array([x, y, z])
                self.xyzlim = np.max([self.xyzlim, xyzlim], axis=0)
            elif len(xyz.shape) == 2:
                # curve points
                xyzlim = np.max(np.abs(xyz), axis=0)
                self.xyzlim = np.max([self.xyzlim, xyzlim], axis=0)
            else:
                raise ValueError()
        else:
            raise ValueError()

    def __validate_surface_selection(self, selection) -> None:
        if not isinstance(selection, (tuple, list, Surface)):
            raise TypeError(
                "selection must be of type 'Surface' or a tuple or list of such"
            )
        if isinstance(selection, (list, tuple)):
            for item in selection:
                if not isinstance(item, Surface):
                    raise TypeError(
                        f"selection {type(selection).__name__} must only contain items of type 'Surface'"
                    )

    def __organize_surface_selection(self, selection) -> tuple[Surface]:
        if isinstance(selection, list):
            return tuple(selection)
        if isinstance(selection, Surface):
            return (selection,)
        return selection

    def add_curve_points(self, xyz: np.ndarray) -> None:
        """Adds curve xyz points to plot"""
        ax = self.get_ax()
        ax.scatter(xyz[:, 0], xyz[:, 1], xyz[:, 2], color="blue")
        self.__update_axis_limits(xyz)

    def add_mesh_points(self, surfaces) -> None:
        self.__validate_surface_selection(surfaces)
        surfaces = self.__organize_surface_selection(surfaces)
        ax = self.get_ax()
        for surface in surfaces:
            xyz = surface.mesh_points
            self.__update_axis_limits(xyz)
            for i in range(0, xyz.shape[1]):
                for j in range(0, xyz.shape[2]):
                    ax.scatter(xyz[0, i, j], xyz[1, i, j], xyz[2, i, j], color="blue")

    def add_panels(
        self,
        surfaces: Surface | list[Surface] | tuple[Surface],
        restricted_panels: list[int] = None,
        include_normals: bool = False,
        include_vertex_annotation: bool = False,
        facecolor: str = "#0072BD",
        edgecolor: str = "black",
        linewidth: float = 0.5,
        alpha: float = 0.8,
        normalcolor: str = "grey",
    ) -> None:
        """"""
        if restricted_panels is None:
            restricted_panels = []
        self.__validate_surface_selection(surfaces)
        surfaces = self.__organize_surface_selection(surfaces)
        ax = self.get_ax()
        for surface in surfaces:
            for pno, panel in enumerate(surface.panels):
                if pno in restricted_panels:
                    continue
                xyz = np.array([panel[0:3], panel[3:6], panel[6:9], panel[9:12]])
                self.__update_axis_limits(xyz)
                if include_vertex_annotation:
                    ax.scatter(xyz[:, 0], xyz[:, 1], xyz[:, 2], color="blue")
                    for i in range(0, xyz.shape[0]):
                        ax.text(xyz[i, 0], xyz[i, 1], xyz[i, 2], f"{i+1}", color="k")
                if include_normals:
                    self._plot_normals(panel, colors=normalcolor)
                verts = [list(zip(panel[0::3], panel[1::3], panel[2::3]))]
                ax.add_collection3d(
                    Poly3DCollection(
                        verts,
                        facecolors=facecolor,
                        linewidths=linewidth,
                        edgecolors=edgecolor,
                        alpha=alpha,
                    )
                )

    def _plot_normals(self, panel: list, colors: str) -> None:
        ax = self.get_ax()
        panel = np.array(panel)
        xyz1, xyz2, xyz3, xyz4 = panel[0:3], panel[3:6], panel[6:9], panel[9:12]
        point = np.average([xyz1, xyz2, xyz3, xyz4], axis=0)
        a, b = xyz2 - xyz1, xyz4 - xyz1
        cross_product = np.cross(a, b)
        x, y, z = point[0], point[1], point[2]
        u, v, w = cross_product[0], cross_product[1], cross_product[2]
        ax.quiver(
            x,
            y,
            z,
            u,
            v,
            w,
            length=self.panel_normal_length,
            normalize=True,
            colors=colors,
        )

    def show(self):
        ax = self.get_ax()
        xlim = (-np.ceil(self.xyzlim[0]), np.ceil(self.xyzlim[0]))
        ylim = (-np.ceil(self.xyzlim[1]), np.ceil(self.xyzlim[1]))
        zlim = (-np.ceil(self.xyzlim[2]), np.ceil(self.xyzlim[2]))
        ax.set(xlim=xlim)
        ax.set(ylim=ylim)
        ax.set(zlim=zlim)
        plt.show()
