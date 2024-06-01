"""Module containing MshViewer class"""

import numpy as np

from matplotlib import pyplot as plt
from matplotlib import style as mpl_style
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

from pymesh.other.typing import NDArray3
from pymesh.mesh.mesh_generator import MeshGenerator


class MeshViewer:
    """Plots surface panels and normals using matplotlib with seaborn-v0_8 style"""

    def __init__(self, mesh: MeshGenerator) -> None:
        self.panels = mesh.get_panels()
        self.include_vertex_annotation = False
        self.facecolor = "#0072BD"
        self.edgecolor = "black"
        self.linewidth = 0.5
        self.alpha = 0.8
        self.include_normals = True
        self.normallength = 0.2
        self.normalcolor = "grey"
        self.xyzlim = np.array([1, 1, 1])
        plt.close("all")
        mpl_style.use("seaborn-v0_8")
        fig = plt.figure()
        fig.patch.set_facecolor("#EAEAF2")
        ax = fig.add_subplot(projection="3d")
        ax.set_xlabel("X axis")
        ax.set_ylabel("Y axis")
        ax.set_zlabel("Z axis")
        self._ax = ax

    @property
    def normallength(self) -> float | None:
        return self._normallength

    @normallength.setter
    def normallength(self, val) -> None:
        if not isinstance(val, (int, float)):
            if not val is None:
                raise TypeError(f"Expected {val!r} to be int or float")
        if isinstance(val, int):
            val = float(val)
        self._normallength = val

    @property
    def ax(self):
        return self._ax

    @property
    def xyzlim(self) -> NDArray3:
        return self._xyzlim

    @xyzlim.setter
    def xyzlim(self, value: NDArray3):
        if not isinstance(value, np.ndarray):
            raise TypeError("xyzlim must be of type 'ndarray'")
        if not value.shape == (3,):
            raise TypeError("xyzlim must have shape (3,)")
        self._xyzlim = np.ceil(value)

    def _plot_panels(self) -> None:
        for panel in self.panels:
            xyz = np.array([panel[0:3], panel[3:6], panel[6:9], panel[9:12]])
            self.__update_axis_limits(xyz)
            if self.include_vertex_annotation:
                self.ax.scatter(xyz[:, 0], xyz[:, 1], xyz[:, 2], color="blue")
                for i in range(0, xyz.shape[0]):
                    self.ax.text(xyz[i, 0], xyz[i, 1], xyz[i, 2], f"{i+1}", color="k")
            if self.include_normals:
                self._plot_normals(panel, colors=self.normalcolor)
            verts = [list(zip(panel[0::3], panel[1::3], panel[2::3]))]
            self.ax.add_collection3d(
                Poly3DCollection(
                    verts,
                    facecolors=self.facecolor,
                    linewidths=self.linewidth,
                    edgecolors=self.edgecolor,
                    alpha=self.alpha,
                )
            )

    def __update_axis_limits(self, xyz):
        x = np.max(np.abs(xyz[:, 0]))
        y = np.max(np.abs(xyz[:, 1]))
        z = np.max(np.abs(xyz[:, 2]))
        xyzlim = np.max([self.xyzlim, np.array([x, y, z])], axis=0)
        self.xyzlim = xyzlim

    def _plot_normals(self, panel: list, colors: str) -> None:
        panel = np.array(panel)
        xyz1, xyz2, xyz3, xyz4 = panel[0:3], panel[3:6], panel[6:9], panel[9:12]
        point = np.average([xyz1, xyz2, xyz3, xyz4], axis=0)
        cross_product = np.cross(xyz2 - xyz1, xyz4 - xyz1)
        x, y, z = point[0], point[1], point[2]
        u, v, w = cross_product[0], cross_product[1], cross_product[2]
        self.ax.quiver(
            x,
            y,
            z,
            u,
            v,
            w,
            length=self.normallength,
            normalize=True,
            colors=colors,
        )

    def _set_axis_limits(self) -> None:
        """Sets axis limits according to xyzlim if include_normal is False.
        Otherwise, uses the ax.axis("image") algortihm.

        This is done to make sure panels without normals are shown correctly.
        However, ax.axis("image") screws up with .normal_length visually.
        """
        xlim, ylim, zlim = self.xyzlim
        self.ax.set(xlim=(-np.ceil(xlim), np.ceil(xlim)))
        self.ax.set(ylim=(-np.ceil(ylim), np.ceil(ylim)))
        self.ax.set(zlim=(-np.ceil(zlim), np.ceil(zlim)))
        if self.include_normals:
            self.ax.axis("image")

    def show(self) -> None:
        self._plot_panels()
        self._set_axis_limits()
        plt.show()
