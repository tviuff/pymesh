# Package at a Glance

The package is based on object-oriented programming and generates three-dimentional geometry objects, such as points, curves, surfaces and a mesh.

## A Simple Example

### Creating the mesh geometry

```python linenums="1" title="pymesh/examples/vertical-cylinder.py"
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
```

### Inspecting the mesh

A `MeshViewer`, based on the `matplotlib` package, is used to conveniently plot and inspect the surface panels and their normals as shown below.

```python linenums="21"
# Inspect geometry
viewer = MeshViewer(mesh)
viewer.show()
```

![Visualization of panel mesh using MeshViewer](../img/simple-example.png "Visualization of panel mesh using MeshViewer")

### Write the mesh to a geometric data file

The `GDFWriter` takes care of converting the surfaces into a usable .gdf file.

```python linenums="25"
from pathlib import Path

# Write geometry to a gdf file
writer = GDFWriter(mesh)
writer.write(filename=Path("output", "simple-example.gdf"))
```

Above code generates the following text file. For information regarding `GDFWriter` file formatting, the reader is referred to Section 6.1 in the [WAMIT Manual](https://www.wamit.com/manual7.x/v75_manual.pdf).

```txt
auto-generated using the pymesh package
1.000000 9.816000
0 0
40
-1.0000e+00 +0.0000e+00 +0.0000e+00 -9.8079e-01 -1.9509e-01 +0.0000e+00 -9.8079e-01 -1.9509e-01 +2.0000e-01 -1.0000e+00 +0.0000e+00 +2.0000e-01
-9.8079e-01 -1.9509e-01 +0.0000e+00 -9.2388e-01 -3.8268e-01 +0.0000e+00 -9.2388e-01 -3.8268e-01 +2.0000e-01 -9.8079e-01 -1.9509e-01 +2.0000e-01
-9.2388e-01 -3.8268e-01 +0.0000e+00 -8.3147e-01 -5.5557e-01 +0.0000e+00 -8.3147e-01 -5.5557e-01 +2.0000e-01 -9.2388e-01 -3.8268e-01 +2.0000e-01
-8.3147e-01 -5.5557e-01 +0.0000e+00 -7.0711e-01 -7.0711e-01 +0.0000e+00 -7.0711e-01 -7.0711e-01 +2.0000e-01 -8.3147e-01 -5.5557e-01 +2.0000e-01
-7.0711e-01 -7.0711e-01 +0.0000e+00 -5.5557e-01 -8.3147e-01 +0.0000e+00 -5.5557e-01 -8.3147e-01 +2.0000e-01 -7.0711e-01 -7.0711e-01 +2.0000e-01
-5.5557e-01 -8.3147e-01 +0.0000e+00 -3.8268e-01 -9.2388e-01 +0.0000e+00 -3.8268e-01 -9.2388e-01 +2.0000e-01 -5.5557e-01 -8.3147e-01 +2.0000e-01
-3.8268e-01 -9.2388e-01 +0.0000e+00 -1.9509e-01 -9.8079e-01 +0.0000e+00 -1.9509e-01 -9.8079e-01 +2.0000e-01 -3.8268e-01 -9.2388e-01 +2.0000e-01
-1.9509e-01 -9.8079e-01 +0.0000e+00 -6.1232e-17 -1.0000e+00 +0.0000e+00 -6.1232e-17 -1.0000e+00 +2.0000e-01 -1.9509e-01 -9.8079e-01 +2.0000e-01
...
```
