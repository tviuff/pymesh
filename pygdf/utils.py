"""Mdule containing utility functions
"""

import time
from typing import Callable, TypeVar, ParamSpec


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
