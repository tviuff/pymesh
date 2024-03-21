# GDF

Geometry package that handles basic geometry and facilitates the creation of 3-dimensional surface panels. These surface panels are converted into a low-order geometric data file (GDF) for import and use in [WAMIT](https://www.wamit.com/).

## Building 3-dimesional surfaces

`gdf` is based on object-oriented programming and the user will be interacting with the following classes when building the geometry:

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

## Building a simple geometry in Python

```Python
# examples/rectangle.py

from gdf import Point, Line, CoonsPatch, ExponentialDistribution, GDFViewer

point1 = Point(0, 0, 0)
point2 = Point(1, 0, 0)
point3 = Point(1, 1, 0)
point4 = Point(0, 1, 0)

line1 = Line(point1, point2)
line2 = Line(point2, point3)
line3 = Line(point3, point4)
line4 = Line(point4, point1)

surface = CoonsPatch([line1, line3, line2, line4])
surface.flip_normal = True # flips surface panel normals
surface.num_points_u = 5 # specifies number of points along the u dimension
surface.num_points_w = 5 # specifies number of points along the w dimension
surface.dist_u = ExponentialDistribution() # distribution method along the u dimension

surface_selection = CoonsPatch.get_all_surfaces()

viewer = GDFViewer(panel_normal_length=0.5) # specify panel normal length for visualization
viewer.add_panels(surface_selection, include_normals=True) # include panel normals
viewer.show() # plot the surface panels
```

## Inspecting the final geometry

The `GDFViewer` is based on the `matplotlib` package and is used to conveniently plot and inspect the surface panels and their normals as shown in the image below.

![](/images/rectangle.png "Visualization of rectangle surface panels using GDFViewer")

## Writing to a *.gdf* file

The `GDFWriter` takes care of converting the surfaces into a usable *.gdf* file.

## Example files

The `examples` folder contain various use examples of the `gdf` package.

## Resources

- [WAMIT Manual](https://www.wamit.com/manual7.x/v75_manual.pdf)
- [Markdown Guide](https://www.markdownguide.org/basic-syntax/)
- YouTube videos by ArjanCodes:
    - [8 Python Coding Tips](https://www.youtube.com/watch?v=woIkysZytSs)
    - [The Ultimate Guide to Writing Classes](https://www.youtube.com/watch?v=lX9UQp2NwTk)
    - [Cohesion and Coupling](https://www.youtube.com/watch?v=eiDyK_ofPPM)

> *More details about the code beaviour will follow soon.*
