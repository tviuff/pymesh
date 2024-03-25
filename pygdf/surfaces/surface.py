"""Module including surface and coons patch classes
"""

from abc import ABC, abstractmethod
from typing import List

from numpy import ndarray

# ! log fliping of normal :)


class Surface(ABC):
    """Surface abstract class"""

    _normal_is_flipped: bool = False
    _all_surfaces: List = []  # to contain every surface type instanciated

    @classmethod
    def get_all_surfaces(cls) -> List:
        """Returns a list of all generated surfaces, independent of surface class name"""
        return cls._all_surfaces

    @abstractmethod
    def path(self, u: int | float, w: int | float) -> ndarray:
        """Surface path function that returns a point in the physical space.

        u:
        normalized surface dimension parameter between -1 and 1.
        If positive, u is the percentage of the dimension covered
        If negative, the value is added to 1, i.e. the direction is flipped

        w:
        normalized surface dimension parameter between -1 and 1.
        If positive, u is the percentage of the dimension covered
        If negative, the value is added to 1, i.e. the direction is flipped

        return:
        numpy ndarray with shape (3, )
        """

    @property
    @abstractmethod
    def mesh_points(self) -> ndarray:
        """Returns surface mesh points as a numpy ndarray.

        Calling the numpy .shape property will return the tuple
        (3, num_panels_u + 1, num_panels_w + 1), where 3 represents
        the x, y and z coordinates. num_panels_u and num_panels_w
        are the number of panels along each of the two surface
        dimensions.
        """

    def flip_panel_normals(self) -> None:
        """Flips all surface panel normals"""
        self._normal_is_flipped = not self._normal_is_flipped

    @property
    def panels(self) -> List[List[float]]:
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
