# Acknowledgements

The various surface algorithms are based on lectures 48 and 49 from the [Lecture Series on Computer Aided Design](https://www.youtube.com/playlist?list=PLC3EE33F27CF14A06) by Dr. Anoop Chawla and P.V. Madhusudan Rao at the Department of Mechanical Engineering, IIT Delhi.

The implementation of the `ArcPVA` curve path algoithm, as well as all curve `rotate` methods, allows for rotation of a vector around another. The current code implementation is based on [Rodrigues' rotation formula](https://en.wikipedia.org/wiki/Rodrigues%27_rotation_formula).

The curve `mirror` method returns a mirror image of the object, mirrored in a plane defined by a point and a normal vector. The implementation is based on code by [Jean Marie](https://math.stackexchange.com/questions/3927881/reflection-over-planes-in-3d).

During work on the `PyMesh` package, inspiration and guidance has come from various sources. Notable parties are [ArjanCodes](https://arjancodes.com/), [Corey Schafer](https://www.youtube.com/@coreyms) and [Michael Viuff](https://github.com/MichaelViuff).
