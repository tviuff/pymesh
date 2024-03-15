# GDFPY

Geometry package that handles basic geometry and facilitates the creation of 3-dimensional surface panels.<br>
Theses surface panels are converted into a low-order geometric data file (GDF) for import and use in [WAMIT](https://www.wamit.com/).

`gdfpy` is based on object-oriented programming and the user will be interacting with the following classes<br>
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

## Functionality to be implemented

### Code behaviour

The package should use OOP with classes for creating points, curves and surfaces in a 3-dimensional space The points are only as helpers for creation of lines and surfaces. Similarly, the lines are used solely for<br>
generation of surfaces.<br>

The surfaces are used for generation of the final panel mesh and implements the [Coon's Patch](https://youtu.be/TM0GM6xhAoI?t=2090) algorithm.

The mesh will be generated using a combination of `csv` and `logger` to generate the GDF file, following<br>
the protecol in the [WAMIT Manual](https://www.wamit.com/manual7.x/v75_manual.pdf).

> *More details about the code beaviour will follow soon.*

### Modules to use

- `unittests` for setting up test procedures
- `constants` for creating project constants
- `exceptions` for creating custom exceptions
- `logger` for GDF file generation

## Resources

- [WAMIT Manual](https://www.wamit.com/manual7.x/v75_manual.pdf)
- [Markdown Guide](https://www.markdownguide.org/basic-syntax/)
- YouTube videos by ArjanCodes:
    - [8 Python Coding Tips](https://www.youtube.com/watch?v=woIkysZytSs)
    - [The Ultimate Guide to Writing Classes](https://www.youtube.com/watch?v=lX9UQp2NwTk)
    - [Cohesion and Coupling](https://www.youtube.com/watch?v=eiDyK_ofPPM)
