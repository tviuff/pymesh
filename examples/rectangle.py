"""Rectangular surface example"""

import sys, os

sys.path.append(os.path.abspath(os.path.join("..", "pygdf")))

# examples/rectangle.py

from pathlib import Path
from pymesh import (
    Point,
    Line,
    CoonsPatch,
    ExponentialDistribution,
    MeshViewer,
    GDFWriter,
)

point1 = Point(0, 0, 0)
point2 = Point(1, 0, 0)
point3 = Point(1, 1, 0)
point4 = Point(0, 1, 0)

line1 = Line(point1, point2)
line2 = Line(point2, point3)
line3 = Line(point3, point4)
line4 = Line(point4, point1)

surface = CoonsPatch([line1, line3, line2, line4])
surface.flip_normal()  # flips surface normal

# Setting meshing options for the normalized u and w dimensons
surface.mesher.set_u_parameters(
    panel_density=3,  # int specifies number of panels
    distribution=ExponentialDistribution(),  # mesh distributed expoentially
)
surface.mesher.set_w_parameters(
    panel_density=0.2,  # float specifies largest panel length along boundaries
)

surface_selection = CoonsPatch.get_all_surfaces()  # get all instanciated surfaces

viewer = MeshViewer(panel_normal_length=0.5)  # specify panel normal length
viewer.add_panels(surface_selection, include_normals=True)  # include panel normals
viewer.show()  # plot selected surface panels

writer = GDFWriter()
writer.write(surface_selection, filename=Path("output", "rectangle.gdf"))
