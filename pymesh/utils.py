"""Mdule containing utility functions
"""

import time
from typing import Callable, TypeVar, ParamSpec

T = TypeVar("T")
P = ParamSpec("P")

# ! validate_rotate_parameters not working properly !


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


def validate_move_parameters(dx: int | float, dy: int | float, dz: int | float) -> None:
    """Validates parameters for the move method"""
    for val in (dx, dy, dz):
        if not isinstance(val, (int, float)):
            raise TypeError(f"Expected {val!r} to be an int or float")


def validate_rotate_parameters(axis, angle: int | float) -> None:
    """Validates parameters for the rotate method"""
    if not isinstance(angle, (int, float)):
        raise TypeError(f"Expected {angle!r} to be an int or float")


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
