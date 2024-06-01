"""Package utility functions.

Geometry helder functions:
    - rotate_point_xyz
    - mirror_point_xyz

Validation functions:
    - validate_curve_path_parameters
    - validate_surface_path_parameters

Benchmark functions:
    - time_it
"""

import math
import time

import numpy as np

from pymesh.typing import NDArray3


def time_it(func):
    """Wrapper function used to time function execution time"""

    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print(
            f"Exceution of '{func.__name__}' took {round((end - start) * 1000)} mil sec."
        )
        return result

    return wrapper


def rotate_point_xyz(
    x: int | float,
    y: int | float,
    z: int | float,
    angle: int | float,
    a: int | float,
    b: int | float,
    c: int | float,
    x0: int | float = 0.0,
    y0: int | float = 0.0,
    z0: int | float = 0.0,
) -> NDArray3:
    """Rotates point around an axis.

    Implementation based on [WikiPedia](https://en.wikipedia.org/wiki/Rodrigues%27_rotation_formula).

    Args:
        angle (int | float): Angle in radians
            Poitive direction defined as counter-clockwise,
            based on the right-hand rule.
        a (int | float): Axis vector x direction.
        b (int | float): Axis vector y direction.
        c (int | float): Axis vector z direction.
        x0 (int | float, optional): Axis base x coordinate
            Default is origin of coordinate system.
        y0 (int | float, optional): Axis base y coordinate
            Default is origin of coordinate system.
        z0 (int | float, optional): Axis base z coordinate
            Default is origin of coordinate system.

    Returns:
        (NDArray3): Rotated point xyz coordinates
            given as a numpy array shaped (3,)

    Raises:
        TypeError: If input value are not of type int or float.
    """
    for val in (x, y, z, angle, a, b, c, x0, y0, z0):
        if not isinstance(val, (int, float)):
            raise TypeError(f"Expected {val!r} to be int or float")
    xyz = np.array([x, y, z])
    xyz0 = np.array([x0, y0, z0])
    abc = np.array([a, b, c])
    avec = abc / math.sqrt(np.sum(abc**2))
    pvec = xyz - xyz0
    part1 = pvec * math.cos(angle)
    part2 = np.cross(avec, pvec) * math.sin(angle)
    part3 = avec * np.dot(avec, pvec) * (1 - math.cos(angle))
    return xyz0 + part1 + part2 + part3


def mirror_point_xyz(
    x: int | float,
    y: int | float,
    z: int | float,
    a: int | float,
    b: int | float,
    c: int | float,
    x0: int | float = 0.0,
    y0: int | float = 0.0,
    z0: int | float = 0.0,
) -> NDArray3:
    """Mirrors xyz point in a plane.

    Implementation based on formulation by [Jean Marie](https://math.stackexchange.com/questions/3927881/reflection-over-planes-in-3d).

    Args:
        x (int | float): Point x coordinate.
        y (int | float): Point y coordinate.
        z (int | float): Point z coordinate.
        a (int | float): Plane normal vector x dimension.
        b (int | float): Plane normal vector y dimension.
        c (int | float): Plane normal vector z dimension.
        x0 (int | float, optional): Plane normal vector base x coordinate
            Default is origin of coordinate system.
        y0 (int | float, optional): Plane normal vector base y coordinate
            Default is origin of coordinate system.
        z0 (int | float, optional): Plane normal vector base z coordinate
            Default is origin of coordinate system.

    Returns:
        NDArray3: Rotated point xyz coordinates
            given as a numpy array shaped (3,)

    Raises:
        TypeError: If input value are not of type int or float.
    """
    for val in (x, y, z, a, b, c, x0, y0, z0):
        if not isinstance(val, (int, float)):
            raise TypeError(f"Expected {val!r} to be int or float")
    xyz = np.array([x, y, z])
    xyz0 = np.array([x0, y0, z0])
    abc = np.array([a, b, c])
    a, b, c = abc / math.sqrt(np.sum(abc**2))
    transformation_matrix = np.array(
        [
            [1 - 2 * a * a, -2 * a * b, -2 * a * c],
            [-2 * a * b, 1 - 2 * b * b, -2 * b * c],
            [-2 * a * c, -2 * b * c, 1 - 2 * c * c],
        ]
    )
    return transformation_matrix.dot(xyz - xyz0) + xyz0


def validate_curve_path_parameters(u: int | float, flip: bool = False) -> float:
    """Validates the normalized curve path parameter.

    Args:
    u (int | float): Normalized path parameter between 0 and 1.
    flip (bool, optional): Default if False. If True,
        then u = (1 - u), i.e. the direction is flipped.


    Returns:
        u (float): Normalized path paremeter between 0 and 1.

    Raises:
        TypeError: If u is not of type int or float
        ValueError: If u is not part of the number set [0 1].
    """
    if not isinstance(u, (int, float)):
        raise TypeError(f"Expected an int or float number, but got {u!r}")
    if isinstance(u, int):
        u = float(u)
    if u < 0 or 1 < u:
        raise ValueError(f"Expected a value between 0 and 1 but got {u!r}")
    if flip:
        u = 1 - u
    return u


def validate_surface_path_parameters(
    u: int | float, w: int | float, uflip: bool = False, wflip: bool = False
) -> tuple[float, float]:
    """Validates the normalized surface path parameter.

    Args:
        u (int | float): Normalized path parameter between 0 and 1.
        w (int | float): Normalized path parameter between 0 and 1.
        uflip (bool, optional): Default is False. If True,
            then u = (1 - u), i.e. the direction is flipped.
        wflip (bool, optional): Default is False. If True,
            then w = (1 - w), i.e. the direction is flipped.

    Returns:
        (tuple): Tuple (u, w) with normalized parameters btween 0 and 1.

    Raises:
        TypeError: If u or w is not of type int or float
        ValueError: If u or w is not part of the number set [0 1].
    """
    return (
        validate_curve_path_parameters(u, uflip),
        validate_curve_path_parameters(w, wflip),
    )
