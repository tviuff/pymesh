```py linenums="1"" title="pymesh/examples/simple-example.py"
from pathlib import Path

from pymesh import Point, Line, Arc3P, SweptSurface
from pymesh import MeshGenerator, MeshViewer, GDFWriter

# Create 3D points based on x, y and z values
p1 = Point(0, 0, 0)
p2 = Point(1, 0, 0)
p3 = Point(0, 1, 0)
p4 = Point(0, 0, 1)

# Create the curves from the points
arc = Arc3P(centre=p1, start=p2, end=p3)
line = Line(start=p1, end=p4)

# Create a surface from the curves
surface = SweptSurface(curve=arc, sweeper=line)

# Initialize the mesh and add the surface to it
mesh = MeshGenerator()
mesh.add_surface(surface)

# Inspect the mesh geometry
viewer = MeshViewer(mesh)
viewer.show()

# Write mesh to a geometric data file
writer = GDFWriter(mesh)
writer.write(filename=Path("output", "simple-example.gdf"))
```
