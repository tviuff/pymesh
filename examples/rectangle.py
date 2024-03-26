"""Rectangular surface example"""

import sys, os

sys.path.append(os.path.abspath(os.path.join("..", "pygdf")))

# examples/rectangle.py

from pathlib import Path
from pymesh import (
    Point,
    Line,
    CoonsPatch,
    LinearDistribution,
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
surface.flip_panel_normals()  # flips surface panel normals

# Setting meshing options for the normalized u and w dimensons
surface.mesher.panel_densities = (
    3,  # int specifies number of panels
    0.2,  # float specifies largest panel length along boundaries
)
surface.mesher.mesh_distributions = (
    ExponentialDistribution(),  # mesh distributed expoentially
    LinearDistribution(),  # mesh distributed linearly
)

# Setting meshing options for the normalized u and w dimensons
surface.panel_density_u = 3  # int specifies number of panels
surface.panel_density_w = 0.2  # float specifies largest panel length along boundaries
surface.boundary_distribution_u = ExponentialDistribution()  # mesh distribution type

surface_selection = CoonsPatch.get_all_surfaces()  # get all instanciated surfaces

viewer = MeshViewer(panel_normal_length=0.5)  # specify panel normal length
viewer.add_panels(surface_selection, include_normals=True)  # include panel normals
viewer.show()  # plot selected surface panels

writer = GDFWriter()
writer.write(surface_selection, filename=Path("output", "rectangle.gdf"))
