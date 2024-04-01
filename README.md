# PYMESH geometry package overview

The `pymesh` package handles basic geometry and facilitates the creation of 3-dimensional surface panels. These surface panels are converted into a low-order geometric data file for import and use in [WAMIT](https://www.wamit.com/).

> *Sections on installation coming soon.*

## Generating, inspecting and writing 3-dimesional surface panels to a .gdf file

The package is based on object-oriented programming and the user will be interacting with the following classes when building the geometry:

- Point:
    - `Point(x, y, z)` creates a point in 3-dimentional space
- Curves:
    - `Line(Point, Point)` creates a straight line between two points
    - `Arc3P(Point, Point, Point)` creates a circular arc defined by a center point, a starting point and an ending point
    - `ArcPVA(Point, angle, a, b, c, x0, y0, z0)` creates a circular arc based on a point swept by an angle around a vector defined by (a, b, c, x0, y0, z0).
- Surfaces:
    - `PlaneSurface(Point, Point, Point)` creates a plane surface based on three corner points.
    - `BilinearSurface(Point, Point, Point, Point)` creates a bilinear surface based on four corner points.
    - `RuledSurface(Curve, Curve)` creates a ruled surface based on two opposing boundary curves.
    - `SweptSurface(Curve, Curve)` creates a surface by sweeping a curve along the path of another.
    - `CoonsPatch([Curve, Curve, Curve, Curve])` creates a surface using four boundary curves.
- Mesh:
    - `mesh = MeshGenerator()` initializes the mesh and adds surfaces to it using `.mesh.add_surface()`.
    - `viewer = MeshViewer(mesh)` handles visualization of the mesh and shows the final plot using the method `viewer.show()`.
- Output:
    - `writer = GDFWriter(mesh)` handles writing mesh to a .gdf file using the method `writer.write()`.

### Building a simple geometry in Python

```Python
# /examples/cylinder.py

import math
from pathlib import Path

from pymesh import Point, Line, Arc3P, ArcPVA, PlaneSurface, RuledSurface, SweptSurface
from pymesh import MeshGenerator, ExponentialDistribution
from pymesh import MeshViewer, GDFWriter

DIAMETER = 2.0
RATIO = 0.4
DEPTH = 5

# Create oOne quarter of the circle plate inner part
point00 = Point(0, 0, -DEPTH)
point10 = Point(RATIO * DIAMETER / 2, 0, -DEPTH)
point01 = Point(0, RATIO * DIAMETER / 2, -DEPTH)
PlaneSurface(point00, point10, point01).flip_normal()

# Create one quarter of the circle plate outer part
point11 = Point(RATIO * DIAMETER / 2, RATIO * DIAMETER / 2, -DEPTH)
point11c = Point(DIAMETER / 2 / math.sqrt(2), DIAMETER / 2 / math.sqrt(2), -DEPTH)
point10c = Point(DIAMETER / 2, 0, -DEPTH)
point01c = Point(0, DIAMETER / 2, -DEPTH)
line10 = Line(point10, point11)
arc10 = Arc3P(point00, point10c, point11c)
RuledSurface(line10, arc10).copy().mirror(a=-1, b=-1, c=0).flip_normal()

# Cretae a full circular plate by copying and rotating existing surfaces
for surface in RuledSurface.get_all_surfaces():
    for angle in (90, 180, 270):
        surface.copy().rotate(angle * math.pi / 180, a=0, b=0, c=1)

# Add surfaces to the mesh generator and set mesh settings
mesh = MeshGenerator()
for surface in RuledSurface.get_all_surfaces():
    mesh.add_surface(surface, density_u=0.2, density_w=0.2)

# Create cylinder surface
circle = ArcPVA(Point(DIAMETER / 2, 0, -DEPTH), 2 * math.pi, a=0, b=0, c=1)
line = Line(Point(0, 0, -DEPTH), Point(0, 0, 0))
surface_cylinder = SweptSurface(circle, line)

# Add cylinder surface to the mesh generator and set mesh settings
mesh.add_surface(
    surface_cylinder,
    density_u=0.2,  # float indicating panel length
    density_w=20,  # int specifying numper of panels
    distribution_w=ExponentialDistribution(flip_direction=True),
)

viewer = MeshViewer(mesh)
viewer.show()

writer = GDFWriter(mesh)
writer.write(filename=Path("output", "cylinder.gdf"))
```

### Inspecting the final geometry

A `MeshViewer`, based on the `matplotlib` package, is used to conveniently plot and inspect the surface panels and their normals as shown in the image below.

```Python
# /examples/cylinder.py

viewer = MeshViewer(mesh)
viewer.show()
```

![](/images/rectangle.png "Visualization of rectangle surface panels using MeshViewer")

### Writing to a geometric data file

The `GDFWriter` takes care of converting the surfaces into a usable .gdf file.

```Python
# /examples/cylinder.py

writer = GDFWriter(mesh)
writer.write(filename=Path("output", "cylinder.gdf"))
```

Above code generates the following `/output/cylinder.gdf` output. For information regarding `GDFWriter` file formatting, the reader is referred to Section 6.1 in the [WAMIT Manual](https://www.wamit.com/manual7.x/v75_manual.pdf).

```
auto-generated using the pymesh package
1.000000 9.816000
0 0
752
+0.0000e+00 +2.0000e-01 -5.0000e+00 +2.0000e-01 +2.0000e-01 -5.0000e+00 +2.0000e-01 +0.0000e+00 -5.0000e+00 +0.0000e+00 +0.0000e+00 -5.0000e+00
+2.0000e-01 +2.0000e-01 -5.0000e+00 +4.0000e-01 +2.0000e-01 -5.0000e+00 +4.0000e-01 +0.0000e+00 -5.0000e+00 +2.0000e-01 +0.0000e+00 -5.0000e+00
+0.0000e+00 +4.0000e-01 -5.0000e+00 +2.0000e-01 +4.0000e-01 -5.0000e+00 +2.0000e-01 +2.0000e-01 -5.0000e+00 +0.0000e+00 +2.0000e-01 -5.0000e+00
+2.0000e-01 +4.0000e-01 -5.0000e+00 +4.0000e-01 +4.0000e-01 -5.0000e+00 +4.0000e-01 +2.0000e-01 -5.0000e+00 +2.0000e-01 +2.0000e-01 -5.0000e+00
+4.0000e-01 +0.0000e+00 -5.0000e+00 +4.0000e-01 +1.0000e-01 -5.0000e+00 +5.9360e-01 +1.3170e-01 -5.0000e+00 +6.0000e-01 +0.0000e+00 -5.0000e+00
+4.0000e-01 +1.0000e-01 -5.0000e+00 +4.0000e-01 +2.0000e-01 -5.0000e+00 +5.7463e-01 +2.6089e-01 -5.0000e+00 +5.9360e-01 +1.3170e-01 -5.0000e+00
+4.0000e-01 +2.0000e-01 -5.0000e+00 +4.0000e-01 +3.0000e-01 -5.0000e+00 +5.4382e-01 +3.8519e-01 -5.0000e+00 +5.7463e-01 +2.6089e-01 -5.0000e+00
+4.0000e-01 +3.0000e-01 -5.0000e+00 +4.0000e-01 +4.0000e-01 -5.0000e+00 +5.0237e-01 +5.0237e-01 -5.0000e+00 +5.4382e-01 +3.8519e-01 -5.0000e+00
+6.0000e-01 +0.0000e+00 -5.0000e+00 +5.9360e-01 +1.3170e-01 -5.0000e+00 +7.8719e-01 +1.6339e-01 -5.0000e+00 +8.0000e-01 +0.0000e+00 -5.0000e+00
...
```

## Acknowledgements

The various surface algorithms are based on lectures 48 and 49 from the [Lecture Series on Computer Aided Design](https://www.youtube.com/playlist?list=PLC3EE33F27CF14A06) by Dr. Anoop Chawla and P.V. Madhusudan Rao at the Department of Mechanical Engineering, IIT Delhi.

The `ArcPVA` curve path algotihm (re-used in the `rotate` method) allows for rotation of a point or vector around a given axis. The implementation is based on [WikiPedia](https://en.wikipedia.org/wiki/Rodrigues%27_rotation_formula).

The `mirror` method returns a mirror image of the object, mirrored in a plane defined by a point and a normal vector. The implementation is based on code by [Jean Marie](https://math.stackexchange.com/questions/3927881/reflection-over-planes-in-3d).

During work on the `pymesh` package, inspiration and guidance has come from various sources. Notable parties are [ArjanCodes](https://arjancodes.com/) and [Corey Schafer](https://www.youtube.com/@coreyms).
