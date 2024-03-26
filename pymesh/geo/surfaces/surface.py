"""Module including surface and coons patch classes
"""

from abc import ABC, abstractmethod
from collections.abc import Callable

import numpy as np

from pymesh.geo.curves.curve import validate_curve_path_parameters
from pymesh.mesh.surface_mesh_generator import SurfaceMeshGenerator
from pymesh.utils.typing import NDArray3, NDArray3xNxN

# ! log fliping of normal :)


class Surface(ABC):
    """Surface abstract class"""

    _mesher: SurfaceMeshGenerator | None = None
    _normal_is_flipped: bool = False
    _all_surfaces: list = []  # to contain every surface type instanciated

    @property
    def mesher(self) -> SurfaceMeshGenerator:
        if self._mesher is None:
            raise AttributeError(
                "The mesher property is None. Try using ._set_mesh_generator()."
            )
        return self._mesher

    def _set_mesh_generator(self, mesher: SurfaceMeshGenerator, force=False):
        """Sets a surface mesh generator if force=True"""
        if force:
            if not isinstance(mesher, SurfaceMeshGenerator):
                raise TypeError(
                    f"Expected {mesher!r} to an instance of {SurfaceMeshGenerator!r}"
                )
            self._mesher = mesher
        else:
            raise AttributeError("Not possible to set a mesher attribute")

    @classmethod
    def get_all_surfaces(cls) -> list:
        """Returns a list of all generated surfaces, independent of surface class name"""
        return cls._all_surfaces

    def flip_panel_normals(self) -> None:
        """Flips all surface panel normals"""
        self._normal_is_flipped = not self._normal_is_flipped

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
    @abstractmethod
    def mesh_points(self) -> NDArray3xNxN[np.float64]:
        """Returns surface mesh points as a numpy ndarray.

        Calling the numpy .shape property will return the tuple
        (3, num_panels_u + 1, num_panels_w + 1), where 3 represents
        the x, y and z coordinates. num_panels_u and num_panels_w
        are the number of panels along each of the two surface
        dimensions.
        """

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
                if self._normal_is_flipped:
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


def validate_surface_path_parameters(
    u: int | float, w: int | float, uflip: bool, wflip: bool
) -> tuple[float, float]:
    """Validates the normalized surface path parameter.

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
    return validate_curve_path_parameters(u, uflip), validate_curve_path_parameters(
        w, wflip
    )
