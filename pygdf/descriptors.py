"""Module containing generic class attribute descriptors
"""

from abc import ABC, abstractmethod
from typing import Tuple

from numpy import ndarray


class Validator(ABC):
    """Descriptor used for validating instance attributes of other classes.
    Based on: https://docs.python.org/3/howto/descriptor.html#validator-class.
    """

    return_type = None

    def __set_name__(self, obj, name):
        self.private_name = "_" + name  # pylint: disable=attribute-defined-outside-init

    def __get__(self, obj, objtype=None):
        return getattr(obj, self.private_name)

    def __set__(self, obj, value):
        self.validate(value)
        value_of_type = self.convert_to_type(value)
        setattr(obj, self.private_name, value_of_type)

    def convert_to_type(self, value):
        if self.return_type is None:
            return value
        return self.return_type(value)  # pylint: disable=not-callable

    @abstractmethod
    def validate(self, value):
        pass


class AsNumber(Validator):
    """Number descriptor validating int or float and setting type according to return_type.
    Based on: https://docs.python.org/3/howto/descriptor.html#custom-validators.
    """

    def __init__(
        self,
        minvalue: int | float = None,
        maxvalue: int | float = None,
        return_type: type = None,
    ):
        self.minvalue = minvalue
        self.maxvalue = maxvalue
        self.return_type = return_type

    def validate(self, value):
        if not isinstance(value, (int, float)):
            raise TypeError(f"Expected {value!r} to be an int or float")
        if self.minvalue is not None and value < self.minvalue:
            raise ValueError(f"Expected {value!r} to be at least {self.minvalue!r}")
        if self.maxvalue is not None and value > self.maxvalue:
            raise ValueError(f"Expected {value!r} to be no more than {self.maxvalue!r}")


class AsInstanceOf(Validator):
    """Descriptor validating that object is an instance of a specified class."""

    def __init__(self, cls):
        self.cls = cls

    def validate(self, value):
        if not isinstance(value, self.cls):
            raise TypeError(f"Expected {value!r} to be an instance of {self.cls!r}")


class AsNDArray(Validator):
    """Descriptor validating that object is an instance of a numpy ndarray."""

    def __init__(self, shape: Tuple[int]):
        self.shape = shape

    def validate(self, arr):
        if not isinstance(arr, ndarray):
            raise TypeError(f"Expected {arr!r} to be an instance of {ndarray!r}")
        assert (
            arr.shape == self.shape
        ), f"Expected shape to be {self.shape!r} but received {arr.shape!r}"
