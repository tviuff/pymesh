"""Mdule containing utility functions
"""

import math
import time
from typing import Callable, TypeVar, ParamSpec

import numpy as np

from pymesh.typing import NDArray3

T = TypeVar("T")
P = ParamSpec("P")


def copy_doc(wrapper: Callable[P, T]):
    """Copies the doc string of the given function to another.
    This function is intended to be used as a decorator.

    .. code-block:: python3

        def foo(x: int, y: int) -> str:
        '''I have a docstring and arguments'''
            ...

        @copy_doc(foo)
        def bar():
            ...
    """

    def decorator(func: Callable) -> Callable[P, T]:
        func.__doc__ = wrapper.__doc__
        return func

    return decorator


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
    x0: int | float,
    y0: int | float,
    z0: int | float,
) -> NDArray3:
    """Rotates point around an axis.

    angle: defined in radians with poitive diriction being
    counter-clockwise, based on the right-hand rule.
    a, b, c: axis vector direction.
    x0, y0, z0: axis base, default is origin of coordinate system.

    Implementation based on https://en.wikipedia.org/wiki/Rodrigues%27_rotation_formula.
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


def mirror_point_xyz(x, y, z, a, b, c, x0, y0, z0) -> NDArray3:
    """Mirrors point in a plane.

    Plane is defined by a normal vector (a, b, c) and a point (x0, y0, z0).
    By default x0 = 0.0, y0 = 0.0 and z0 = 0.0.

    Implementation based on https://math.stackexchange.com/questions/3927881/reflection-over-planes-in-3d.
    """
    for val in (a, b, c, x0, y0, z0):
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

    u:
    Normalized path parameter between 0 and 1

    flip:
    Optional, if True then u = (1 - u), i.e. the direction is flipped

    return:
    u
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
    u: int | float, w: int | float, uflip: bool, wflip: bool
) -> tuple[float, float]:
    """Validates the normalized surface path parameter.

    u:
    Normalized path parameter between 0 and 1

    w:
    Normalized path parameter between 0 and 1

    uflip:
    Optional, if True then u = (1 - u), i.e. the direction is flipped

    wflip:
    Optional, if True then u = (1 - u), i.e. the direction is flipped

    return:
    u, w
    """
    return (
        validate_curve_path_parameters(u, uflip),
        validate_curve_path_parameters(w, wflip),
    )
