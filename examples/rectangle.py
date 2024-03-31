"""Rectangular surface example"""

import sys, os

sys.path.append(os.path.abspath(os.path.join("..", "pygdf")))

# examples/rectangle.py

import math
from pathlib import Path
from pymesh import Point, Line, CoonsPatch
from pymesh import MeshGenerator, ExponentialDistribution
from pymesh import MeshViewer, GDFWriter

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

surface_copy = surface.copy()
surface_copy.move(dx=-1, dy=-1)
surface_copy.rotate(90 * math.pi / 180, a=0, b=0, c=1)
surface_copy.mirror(a=0, b=0, c=1, z0=-1)

# Setting meshing options for the normalized u and w dimensons
mesh = MeshGenerator()
for surface in CoonsPatch.get_all_surfaces():
    mesh.add_surface(
        surface,
        density_u=3,  # int specifies number of panels,
        distribution_u=ExponentialDistribution(),  # mesh distributed expoentially
        density_w=0.2,  # float specifies largest panel length along boundaries
    )

viewer = MeshViewer(mesh, panel_normal_length=0.5)  # specify panel normal length
# viewer.add_panels(surface_selection, include_normals=True)  # include panel normals
viewer.show()  # plot selected surface panels

# writer = GDFWriter()
# writer.write(surface_selection, filename=Path("output", "rectangle.gdf"))
