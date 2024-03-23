# GDF geometry package overview

The `gdf` package handles basic geometry and facilitates the creation of 3-dimensional surface panels. These surface panels are converted into a low-order .gdf geometric data file for import and use in [WAMIT](https://www.wamit.com/).

## Generating, inspecting and writing 3-dimesional surface panels to a .gdf file

The `gdf` package is based on object-oriented programming and the user will be interacting with the following classes when building the geometry:

- Points and vectors:
    - `Point(x, y, z)` auxilliary point in 3-dimentional space for creating other points, vectors, curves and surfaces
    - `Vector3D(Point, Point)` auxilliary 3-dimentional vector for creating surfaces
- Curves:
    - `Line(Point, Point)` creates a straight line between two points
    - `Arc3P(Point, Point, Point)` creates a circular arc defined by a center point, a starting point and an ending point
    - `ArcPVA(Point, Vector3D, angle)` creates a circular arc based on a point swept by an angle around a vector axis
- Surfaces:
    - `CoonsPatch([Curve, Curve, Curve, Curve])` creates a 3-dimensional surface using four boundary curves
    - `PlaneSurface(Point, Point, Point)` creates a plane surface based on three points
    - `SweptSurface(Curve, Curve)` creates a surface by sweeping a curve along the path of another

### Building a simple geometry in Python

```Python
# examples/rectangle.py

from pathlib import Path
from gdf import Point, Line, CoonsPatch, ExponentialDistribution, GDFViewer, GDFWriter

point1 = Point(0, 0, 0)
point2 = Point(1, 0, 0)
point3 = Point(1, 1, 0)
point4 = Point(0, 1, 0)

line1 = Line(point1, point2)
line2 = Line(point2, point3)
line3 = Line(point3, point4)
line4 = Line(point4, point1)

surface = CoonsPatch([line1, line3, line2, line4])
surface.flip_panel_normals() # flips surface panel normals

# Setting meshing options for the normalized u and w dimensons
surface.panel_density_u = 3 # int specifies number of panels
surface.panel_density_w = 0.2 # float specifies number of panels per meter
surface.boundary_distribution_u = ExponentialDistribution() # mesh distribution type

surface_selection = CoonsPatch.get_all_surfaces() # get all instanciated surfaces

viewer = GDFViewer(panel_normal_length=0.5) # specify panel normal length for visualization
viewer.add_panels(surface_selection, include_normals=True) # include panel normals
viewer.show() # plot selected surface panels
```

### Inspecting the final geometry

The `GDFViewer` is based on the `matplotlib` package and is used to conveniently plot and inspect the surface panels and their normals as shown in the image below.

![](/images/rectangle.png "Visualization of rectangle surface panels using GDFViewer")

### Writing to a .gdf file

The `GDFWriter` takes care of converting the surfaces into a usable .gdf file.

```Python
# examples/rectangle.py - continued

writer = GDFWriter()
writer.write(surface_selection, filename=Path("output", "rectangle.gdf"))
```

Above code generates the following `output/rectangle.gdf` output. For information regarding `GDFWriter` file formatting, the reader is referred to Section 6.1 in the [WAMIT Manual](https://www.wamit.com/manual7.x/v75_manual.pdf).

```
auto-generated .gdf file using the gdf package
1.000000 9.816000
0 0
15
+0.0000e+00 +2.0000e-01 +0.0000e+00 +2.3024e-01 +2.0000e-01 +0.0000e+00 +2.3024e-01 +0.0000e+00 +0.0000e+00 +0.0000e+00 +0.0000e+00 +0.0000e+00
+2.3024e-01 +2.0000e-01 +0.0000e+00 +5.5156e-01 +2.0000e-01 +0.0000e+00 +5.5156e-01 +0.0000e+00 +0.0000e+00 +2.3024e-01 +0.0000e+00 +0.0000e+00
+5.5156e-01 +2.0000e-01 +0.0000e+00 +1.0000e+00 +2.0000e-01 +0.0000e+00 +1.0000e+00 +0.0000e+00 +0.0000e+00 +5.5156e-01 +0.0000e+00 +0.0000e+00
+0.0000e+00 +4.0000e-01 +0.0000e+00 +2.3024e-01 +4.0000e-01 +0.0000e+00 +2.3024e-01 +2.0000e-01 +0.0000e+00 +0.0000e+00 +2.0000e-01 +0.0000e+00
+2.3024e-01 +4.0000e-01 +0.0000e+00 +5.5156e-01 +4.0000e-01 +0.0000e+00 +5.5156e-01 +2.0000e-01 +0.0000e+00 +2.3024e-01 +2.0000e-01 +0.0000e+00
+5.5156e-01 +4.0000e-01 +0.0000e+00 +1.0000e+00 +4.0000e-01 +0.0000e+00 +1.0000e+00 +2.0000e-01 +0.0000e+00 +5.5156e-01 +2.0000e-01 +0.0000e+00
+0.0000e+00 +6.0000e-01 +0.0000e+00 +2.3024e-01 +6.0000e-01 +0.0000e+00 +2.3024e-01 +4.0000e-01 +0.0000e+00 +0.0000e+00 +4.0000e-01 +0.0000e+00
+2.3024e-01 +6.0000e-01 +0.0000e+00 +5.5156e-01 +6.0000e-01 +0.0000e+00 +5.5156e-01 +4.0000e-01 +0.0000e+00 +2.3024e-01 +4.0000e-01 +0.0000e+00
+5.5156e-01 +6.0000e-01 +0.0000e+00 +1.0000e+00 +6.0000e-01 +0.0000e+00 +1.0000e+00 +4.0000e-01 +0.0000e+00 +5.5156e-01 +4.0000e-01 +0.0000e+00
+0.0000e+00 +8.0000e-01 +0.0000e+00 +2.3024e-01 +8.0000e-01 +0.0000e+00 +2.3024e-01 +6.0000e-01 +0.0000e+00 +0.0000e+00 +6.0000e-01 +0.0000e+00
+2.3024e-01 +8.0000e-01 +0.0000e+00 +5.5156e-01 +8.0000e-01 +0.0000e+00 +5.5156e-01 +6.0000e-01 +0.0000e+00 +2.3024e-01 +6.0000e-01 +0.0000e+00
+5.5156e-01 +8.0000e-01 +0.0000e+00 +1.0000e+00 +8.0000e-01 +0.0000e+00 +1.0000e+00 +6.0000e-01 +0.0000e+00 +5.5156e-01 +6.0000e-01 +0.0000e+00
+0.0000e+00 +1.0000e+00 +0.0000e+00 +2.3024e-01 +1.0000e+00 +0.0000e+00 +2.3024e-01 +8.0000e-01 +0.0000e+00 +0.0000e+00 +8.0000e-01 +0.0000e+00
+2.3024e-01 +1.0000e+00 +0.0000e+00 +5.5156e-01 +1.0000e+00 +0.0000e+00 +5.5156e-01 +8.0000e-01 +0.0000e+00 +2.3024e-01 +8.0000e-01 +0.0000e+00
+5.5156e-01 +1.0000e+00 +0.0000e+00 +1.0000e+00 +1.0000e+00 +0.0000e+00 +1.0000e+00 +8.0000e-01 +0.0000e+00 +5.5156e-01 +8.0000e-01 +0.0000e+00
```

## Example files

The `examples` folder contain various code use examples of the `gdf` package. Noteworthy example files are:

- [Ruled Surface Example](/examples/ruled_surface.py)
- [Swept Surface Example](/examples/swept_surface.py)
- [Bilinear Surface Example](/examples/bilinear_surface.py)
- [Vertical Cylinder Example](/examples/vertical_cylinder.py)

> *More details about the code beaviour will follow soon.*

## Acknowledgements

The various surface algorithms are based on lectures 48 and 49 from the [Lecture Series on Computer Aided Design](https://www.youtube.com/playlist?list=PLC3EE33F27CF14A06) by Dr. Anoop Chawla and P.V. Madhusudan Rao at the Department of Mechanical Engineering, IIT Delhi.

## Other resources

- The [Seven Rules](https://cbea.ms/git-commit/#seven-rules) of a great Git Commit message:
    1. Separate subject from body with a blank line
    1. Limit the subject line to 50 characters
    1. Capitalize the subject line
    1. Do not end the subject line with a period
    1. Use the imperative mood in the subject line, i.e. "Clean your room"
    1. Wrap the body at 72 characters
    1. Use the body to explain what and why vs. how
- [Markdown Guide](https://www.markdownguide.org/basic-syntax/#overview)
