"""Module containing gdf writer class"""

from pathlib import Path
import os

from pygdf.surfaces.surface import Surface


class GDFWriter:
    """Writes surface panels to filename with the extension '.gdf'

    Planes of symmetry:
    isx = True:  The x = 0 plane is a geometric plane of symmetry
    isx = False: The x = 0 plane is not a geometric plane of symmetry
    isy = True:  The y = 0 plane is a geometric plane of symmetry
    isy = False: The y = 0 plane is not a geometric plane of symmetry
    """

    def __init__(
        self,
        ulen: float = 1.0,
        grav: float = 9.816,
        isx: bool = False,
        isy: bool = False,
        header: str = None,
    ) -> None:
        if header is None:
            header = "auto-generated using the pygdf package"
        self.header = header
        self.ulen = ulen
        self.grav = grav
        self.isx = isx
        self.isy = isy

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

    def write(self, surfaces: Surface | list[Surface] | tuple[Surface], filename: Path):
        """Writes surface panels to file"""
        self.__validate_filename(filename)
        self.__validate_content(surfaces)
        surfaces = self.__organize_content(surfaces)
        with open(filename, "w+", encoding="utf-8") as file:
            file.write(f"{self.header}\n")
            file.write(f"{self.ulen:f} {self.grav:f}\n")
            file.write(f"{self.isx:.0f} {self.isy:.0f}\n")
            npan = sum(
                [len([panel for panel in surface.panels]) for surface in surfaces]
            )
            file.write(f"{npan:.0f}\n")
            for surface in surfaces:
                for panel in surface.panels:
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

    def __validate_content(self, content) -> None:
        if not isinstance(content, (tuple, list, Surface)):
            raise TypeError(
                "content must be of type 'Surface' or a tuple or list of such"
            )
        if isinstance(content, (list, tuple)):
            for item in content:
                if not isinstance(item, Surface):
                    raise TypeError(
                        f"content {type(content).__name__} must contain items of type 'Surface'"
                    )

    def __organize_content(self, content) -> tuple[Surface]:
        if isinstance(content, list):
            return tuple(content)
        if isinstance(content, Surface):
            return (content,)
        return content
