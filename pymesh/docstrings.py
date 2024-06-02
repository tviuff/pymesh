"""Package module for testing docstring copy methods.

Note:
    Currently the @copy_docstring implementation does not work!
"""

from typing import Any, Callable, TypeVar, ParamSpec

T = TypeVar("T")
P = ParamSpec("P")


def copy_docstring(wrapper: Callable[P, T]):
    """Copies the docstring of the given function to another.

    This function is intended to be used as a decorator.

    .. code-block:: python3

        def foo(x: int, y: int) -> str:
        '''I have a docstring and arguments'''
            ...

        @copy_docstring(foo)
        def bar():
            ...

    Note:
        Above code block style works with in Visual Studio Code.
    """

    def decorator(func: Callable) -> Callable[P, T]:
        func.__doc__ = wrapper.__doc__
        return func

    return decorator


def test_fn(a: Any) -> Any:
    """Test function.

    Used for checking if the decorator @copy_docstring is working.

    Args:
        a: Input parameter.

    Returns:
        a: Output parameter.
    """
    return a


@copy_docstring(test_fn)
def test_fn_with_copied_docstring(a: Any) -> Any:
    """Dummy docstring, to be replaced."""
    return a


class DocstringTestClass:

    def test_method(self, a: Any) -> Any:
        """Test method.

        Used for checking if the decorator @copy_docstring is working.

        Args:
            a: Input parameter.

        Returns:
            a: Output parameter.
        """
        return a

    @copy_docstring(test_method)
    def test_method_with_copied_docstring(self, a: Any) -> Any:
        """Dummy docstring, to be replaced."""
        return a
