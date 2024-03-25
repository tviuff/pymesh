"""Module containing generic class attribute descriptors
"""

from abc import ABC, abstractmethod
from collections.abc import Callable

import numpy as np

from pygdf.utils.typing import NDArray3


class Validator(ABC):
    """Descriptor used for validating instance attributes of other classes.
    Based on: https://docs.python.org/3/howto/descriptor.html#validator-class.
    """

    return_type: Callable | None = None

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
        if not callable(self.return_type):
            raise TypeError(f"Expected {self.return_type:!r} to be callable")
        return self.return_type(value)  # pylint: disable=not-callable

    @abstractmethod
    def validate(self, value):
        """Validates value based on various relevant criteria"""


class AsNumber(Validator):
    """Number descriptor validating int or float and setting type according to return_type.
    Based on: https://docs.python.org/3/howto/descriptor.html#custom-validators.
    """

    def __init__(
        self,
        minvalue: int | float | None = None,
        maxvalue: int | float | None = None,
        return_type: Callable | None = None,
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

    def __init__(self, shape: tuple[int]):
        self.shape = shape

    def __set__(self, obj, value: NDArray3[np.float64]):
        super().__set__(obj, value)

    def validate(self, arr):
        if not isinstance(arr, np.ndarray):
            raise TypeError(f"Expected {arr!r} to be an instance of {np.ndarray!r}")
        assert (
            arr.shape == self.shape
        ), f"Expected shape to be {self.shape!r} but received {arr.shape!r}"


class AsContainerOf(Validator):
    """"""

    def __init__(
        self,
        container_type,
        item_type,
        min_length: int | None = None,
        max_length: int | None = None,
    ):
        self.container_type = container_type
        self.item_type = item_type
        self.min_length = min_length
        self.max_length = max_length

    def validate(self, value):
        if not isinstance(value, self.container_type):
            raise TypeError(f"Expected {value!r} to be {self.container_type!r}")
        if self.min_length is not None and len(value) < self.min_length:
            raise ValueError(
                f"Expected {self.container_type!r} to have min {self.min_length!r} items"
            )
        if self.max_length is not None and len(value) > self.max_length:
            raise ValueError(
                f"Expected {self.container_type!r} to have max {self.max_length!r} items"
            )
        for item in value:
            if not isinstance(item, self.item_type):
                raise TypeError(f"Expected {item!r} to be {self.item_type!r}")
