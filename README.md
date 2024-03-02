# MESH GENERATOR

The package `mesh generator` is used for creating quadrilateral panel mesh for import and use in [WAMIT](https://www.wamit.com/).<br>
The current implementation only supports creation of Geometric Data File (GDF) as part of the low-order method in WAMIT.

The package is based on Object-Oriented Programming (OOP) and gives the user the ability to use the following classes:

- Points:
    - `Point`
- Curves:
    - `Line`
    - `Arc3` *..to be implemented*
- Surfaces:
    - *..to be implemented*
- Mesh:
    - *..to be implemented*

## Functionality to be implemented

### Code behaviour

The package should use OOP with classes for creating points, curves and surfaces in a 3-dimensional space The points are only as helpers for creation of lines and surfaces. Similarly, the lines are used solely for<br>
generation of surfaces.<br>

The surfaces are used for generation of the final panel mesh and implements the [Coon's Patch](https://youtu.be/TM0GM6xhAoI?t=2090) algorithm.

The mesh will be generated using a combination of `csv` and `logger` to generate the GDF file, following<br>
the protecol in the [WAMIT Manual](https://www.wamit.com/manual7.x/v75_manual.pdf).

> More details about the code beaviour will follow soon.

### Modules to use

- **unittests**, set up test procedures
- **exceptions**, create custom ones
- **logger**, could be smart for later GDF generation

## Resources

- [WAMIT Manual](https://www.wamit.com/manual7.x/v75_manual.pdf)
- [Markdown Guide](https://www.markdownguide.org/basic-syntax/)
- ArjanCodes on YouTube:
    - [8 Python Coding Tips](https://www.youtube.com/watch?v=woIkysZytSs)
    - [The Ultimate Guide to Writing Classes](https://www.youtube.com/watch?v=lX9UQp2NwTk)
    - [Cohesion and Coupling](https://www.youtube.com/watch?v=eiDyK_ofPPM)