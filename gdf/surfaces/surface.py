"""Module including surface and coons patch classes
"""

from abc import ABC, abstractmethod

class Surface(ABC):
    """Surface abstract class"""

    _flip_normal = False
    _all_surfaces = []

    @classmethod
    def get_all_surfaces(cls) -> list:
        return cls._all_surfaces

    @property
    @abstractmethod
    def mesh_points(self):
        """Returns surface mesh points"""

    @property
    def flip_normal(self) -> bool:
        return self._flip_normal

    @flip_normal.setter
    def flip_normal(self, value:bool) -> None:
        if not isinstance(value, bool):
            raise TypeError("flip_normal must e of type 'bool'")
        self._flip_normal = value

    @property
    def panels(self) -> list[list[float]]:
        """Returns list of quadrilateral panels.
        
        Each panel is defined as a list of 12 floating numbers,
        representing the xyz coordinates of the four panel vertices:
        panel = [x0, y0, z0, x1, y1, z1, x2, y2, z2, x3, y3, z3]
        """
        panels = []
        mp = self.mesh_points
        for j in range(0, mp.shape[2]-1):
            for i in range(0, mp.shape[1]-1):
                xyz1, xyz2, xyz3, xyz4 = mp[:,i,j], mp[:,i+1,j], mp[:,i+1,j+1], mp[:,i,j+1]
                if self.flip_normal:
                    xyz1, xyz2, xyz3, xyz4 = xyz4, xyz3, xyz2, xyz1
                panels.append([xyz1[0], xyz1[1], xyz1[2],
                               xyz2[0], xyz2[1], xyz2[2],
                               xyz3[0], xyz3[1], xyz3[2],
                               xyz4[0], xyz4[1], xyz4[2]])
        return panels
