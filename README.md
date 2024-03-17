# GDF

Geometry package that handles basic geometry and facilitates the creation of 3-dimensional surface panels.<br>
Theses surface panels are converted into a low-order geometric data file (GDF) for import and use in [WAMIT](https://www.wamit.com/).

## Building 3-dimesional surfaces

`gdf` is based on object-oriented programming and the user will be interacting with the following classes<br>
when building the geometry:

- Points and vectors:
    - `Point(x, y, z)` auxilliary point in 3-dimentional space for creating other points, vectors, curves and surfaces
    - `Vector3D(Point, Point)` auxilliary 3-dimentional vector for creating surfaces
- Curves:
    - `Line(Point, Point)` creates a straight line between two points
    - `Arc3P(Point, Point, Point)` creates a circular arc defined by a starting point, an ending point and a circle center point
    - `ArcVA(Vector3D, Vector3D, angle)` creates a circular arc based on a vector swept around an axis defined by another vector
- Surfaces:
    - `CoonsPatch(Curve, Curve, Curve, Curve)` creates a 3-dimensional surface using four boundary curves
    - `PlaneSurface(Point, Point, Point)` creates a plane surface based on three points
    - `SweptSurface(Curve, Curve)` creates a surface by sweeping a curve along the path of another

## Inspecting the final geometry

The `GDFViewer` is based on the `matplotlib` package and is used to conveniently plot and inspect the surface panels and their normals.

## Writing to a *.gdf* file

The `GDFWriter` takes care of converting the surfaces into a usable *.gdf* file.

## Resources

- [WAMIT Manual](https://www.wamit.com/manual7.x/v75_manual.pdf)
- [Markdown Guide](https://www.markdownguide.org/basic-syntax/)
- YouTube videos by ArjanCodes:
    - [8 Python Coding Tips](https://www.youtube.com/watch?v=woIkysZytSs)
    - [The Ultimate Guide to Writing Classes](https://www.youtube.com/watch?v=lX9UQp2NwTk)
    - [Cohesion and Coupling](https://www.youtube.com/watch?v=eiDyK_ofPPM)

> *More details about the code beaviour will follow soon.*
