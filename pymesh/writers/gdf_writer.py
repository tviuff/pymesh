"""Module containing GDFWriter class"""

from pathlib import Path
import os

from pymesh.mesh.mesh_generator import MeshGenerator

# ! fix typing of NDArray cases


class GDFWriter:
    """Writes surface panels to filename with the extension '.gdf'

    Planes of symmetry:
    isx = True:  The x = 0 plane is a geometric plane of symmetry
    isx = False: The x = 0 plane is not a geometric plane of symmetry
    isy = True:  The y = 0 plane is a geometric plane of symmetry
    isy = False: The y = 0 plane is not a geometric plane of symmetry

    Attributes:
        ulen (float): unit length
        grav (float): gravitational constant
        isx (bool): symmetry in x=0
        isy (bool): symmetry in y=0
        header (str): header line in output file
    """

    def __init__(
        self,
        mesh: MeshGenerator,
        ulen: float = 1.0,
        grav: float = 9.816,
        isx: bool = False,
        isy: bool = False,
        header: str = None,
    ) -> None:
        self.panels = mesh.get_panels()
        self.ulen = ulen
        self.grav = grav
        self.isx = isx
        self.isy = isy
        if header is None:
            header = "auto-generated using the pymesh package"
        self.header = header

    @property
    def header(self) -> str:
        return self._header

    @header.setter
    def header(self, value: str) -> None:
        if not isinstance(value, str):
            raise TypeError("header must be of type 'str'")
        if len(value) > 72:
            raise ValueError("header text string is more than 72 characters")
        self._header = value

    @property
    def ulen(self) -> float:
        return self._ulen

    @ulen.setter
    def ulen(self, value: float) -> None:
        if not isinstance(value, float):
            raise TypeError("ulen must be of type 'float'")
        if value <= 0:
            raise ValueError("ulen must be positive")
        self._ulen = value

    @property
    def grav(self) -> float:
        return self._grav

    @grav.setter
    def grav(self, value: float) -> None:
        if not isinstance(value, float):
            raise TypeError("grav must be of type 'float'")
        if value <= 0:
            raise ValueError("grav must be positive")
        self._grav = value

    @property
    def isx(self) -> bool:
        return self._isx

    @isx.setter
    def isx(self, value: bool) -> None:
        if not isinstance(value, bool):
            raise TypeError("isx must be of type 'bool'")
        self._isx = value

    @property
    def isy(self) -> bool:
        return self._isy

    @isy.setter
    def isy(self, value: bool) -> None:
        if not isinstance(value, bool):
            raise TypeError("isy must be of type 'bool'")
        self._isy = value

    def write(self, filename: Path):
        """Writes surface panels to file"""
        self.__validate_filename(filename)
        with open(filename, "w+", encoding="utf-8") as file:
            file.write(f"{self.header}\n")
            file.write(f"{self.ulen:f} {self.grav:f}\n")
            file.write(f"{self.isx:.0f} {self.isy:.0f}\n")
            npan = len(self.panels)
            file.write(f"{npan:.0f}\n")
            for panel in self.panels:
                txt = ""
                for i, coord in enumerate(panel):
                    txt_space = "" if i == 0 else " "
                    txt += f"{txt_space}{coord:+.4e}"
                file.write(f"{txt}\n")

    def __validate_filename(self, filename: Path) -> None:
        if not isinstance(filename, Path):
            raise TypeError("filename musth be of type 'Path'")
        if not self.__is_gdf(filename):
            raise TypeError("filename must have the extension '.gdf'")

    def __is_gdf(self, filename) -> bool:
        _, extension = os.path.splitext(filename)
        extension = extension.lower()
        return extension == ".gdf"
