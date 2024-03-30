"""Module containing the Surface class"""

from abc import ABC, abstractmethod
from collections.abc import Callable
from typing import Self

import numpy as np

from pymesh.geo.vector3d import Vector3D
from pymesh.mesh.mesh_generator import MeshGenerator
from pymesh.typing import NDArray3, NDArray3xNxN


class Surface(ABC):
    """Surface abstract class"""

    __normal_is_flipped: bool = False
    _all_surfaces: list = []  # to contain every surface type instanciated

    def __init__(self):
        self._set_mesh_generator(
            MeshGenerator(self.get_path(), self.get_max_lengths()), force=True
        )

    @property
    def mesher(self) -> MeshGenerator:
        """Used for setting mesh properties"""
        return self._mesher

    @mesher.setter
    def mesher(self, value) -> None:
        if not isinstance(value, MeshGenerator):
            raise TypeError(f"Expected {value!r} to be an instance of MeshGenerator")
        self._mesher = value

    def _set_mesh_generator(self, mesher: MeshGenerator, force=False):
        """Sets a surface mesh generator if force=True"""
        if force:
            if not isinstance(mesher, MeshGenerator):
                raise TypeError(
                    f"Expected {mesher!r} to an instance of {MeshGenerator!r}"
                )
            self._mesher = mesher
        else:
            raise AttributeError("Not possible to set a mesher attribute")

    @classmethod
    def get_all_surfaces(cls) -> list:
        """Returns a list of all generated surfaces, independent of surface class name"""
        return cls._all_surfaces

    def flip_normal(self) -> None:
        """Flips surface normal"""
        self.__normal_is_flipped = not self.__normal_is_flipped

    @abstractmethod
    def copy(self) -> Self:
        """Returns a recursive copy of surface instance"""

    @abstractmethod
    def move(
        self, dx: int | float = 0.0, dy: int | float = 0.0, dz: int | float = 0.0
    ) -> Self:
        """Moves the surface a given relative position"""

    @abstractmethod
    def rotate(self, axis: Vector3D, angle: int | float) -> Self:
        """Rotates the surface around an axis.

        axis: vector axis the rotation is performed around

        angle: defined in radians with poitive diriction being
        counter-clockwise, based on the right-hand rule
        """

    def get_path(
        self,
    ) -> Callable[[int | float, int | float, bool, bool], NDArray3[np.float64]]:
        """Returns surface path function"""
        return self.path

    @abstractmethod
    def path(
        self, u: int | float, w: int | float, uflip: bool = False, wflip: bool = False
    ) -> NDArray3[np.float64]:
        """Surface path function that returns a point in physical space.

        u:
        Normalized path parameter between 0 and 1

        w:
        Normalized path parameter between 0 and 1

        uflip:
        Optional, if True then u = (1 - u), i.e. the direction is flipped

        wflip:
        Optional, if True then u = (1 - u), i.e. the direction is flipped

        return:
        u, w
        """

    @abstractmethod
    def get_max_lengths(self) -> tuple[float]:
        """Returns a tuple of shape (2,) with the longest surface
        boundary length along each of the u and w dimensions. Indices
        0 and 1 represent the u and w dimensions, respectively.
        """

    @property
    def mesh_points(self) -> NDArray3xNxN[np.float64]:
        """Returns surface mesh points as a numpy ndarray.

        Calling the numpy .shape property will return the tuple
        (3, num_panels_u + 1, num_panels_w + 1), where 3 represents
        the x, y and z coordinates. num_panels_u and num_panels_w
        are the number of panels along each of the two surface
        dimensions.
        """
        return self.mesher.generate_mesh_points()

    @property
    def panels(self) -> list[list[float]]:
        """Returns list of quadrilateral panels.

        Each panel is defined as a list of 12 floating numbers,
        representing the xyz coordinates of the four panel vertices:
        panel = [x0, y0, z0, x1, y1, z1, x2, y2, z2, x3, y3, z3]
        """
        panels = []
        mp = self.mesh_points
        for j in range(0, mp.shape[2] - 1):
            for i in range(0, mp.shape[1] - 1):
                xyz1 = mp[:, i, j]
                xyz2 = mp[:, i + 1, j]
                xyz3 = mp[:, i + 1, j + 1]
                xyz4 = mp[:, i, j + 1]
                if self.__normal_is_flipped:
                    xyz1, xyz2, xyz3, xyz4 = xyz4, xyz3, xyz2, xyz1
                panels.append(
                    [
                        xyz1[0],
                        xyz1[1],
                        xyz1[2],
                        xyz2[0],
                        xyz2[1],
                        xyz2[2],
                        xyz3[0],
                        xyz3[1],
                        xyz3[2],
                        xyz4[0],
                        xyz4[1],
                        xyz4[2],
                    ]
                )
        return panels
