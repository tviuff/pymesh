"""Module containing generic class attribute descriptors
"""

from abc import ABC, abstractmethod
from collections.abc import Callable

import numpy as np

from pymesh.other.typing import NDArray3


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

    def __init__(
        self,
        shape: tuple[int],
    ):
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


###############################################
### OTHER DESCRIPTORS THAT DOES NOT WORK... ###
###############################################


class Property(ABC):
    """Emulate PyProperty_Type() in Objects/descrobject.c

    Copied from https://docs.python.org/3/howto/descriptor.html#properties
    """

    return_type: Callable | None = None

    def __init__(self, fget=None, fset=None, fdel=None, doc=None):
        self.fget = fget
        self.fset = fset
        self.fdel = fdel
        if doc is None and fget is not None:
            doc = fget.__doc__
        self.__doc__ = doc
        self._name = ""

    def __set_name__(self, owner, name):
        self._name = name

    def __get__(self, obj, objtype=None):
        if obj is None:
            return self
        if self.fget is None:
            raise AttributeError(
                f"property {self._name!r} of {type(obj).__name__!r} object has no getter"
            )
        return self.fget(obj)

    def __set__(self, obj, value):
        if self.fset is None:
            raise AttributeError(
                f"property {self._name!r} of {type(obj).__name__!r} object has no setter"
            )
        self.validate(value)
        value_of_type = self.convert_to_type(value)
        self.fset(obj, value_of_type)

    def __delete__(self, obj):
        if self.fdel is None:
            raise AttributeError(
                f"property {self._name!r} of {type(obj).__name__!r} object has no deleter"
            )
        self.fdel(obj)

    def getter(self, fget):
        prop = type(self)(fget, self.fset, self.fdel, self.__doc__)
        prop._name = self._name
        return prop

    def setter(self, fset):
        prop = type(self)(self.fget, fset, self.fdel, self.__doc__)
        prop._name = self._name
        return prop

    def deleter(self, fdel):
        prop = type(self)(self.fget, self.fset, fdel, self.__doc__)
        prop._name = self._name
        return prop

    def convert_to_type(self, value):
        if self.return_type is None:
            return value
        if not callable(self.return_type):
            raise TypeError(f"Expected {self.return_type:!r} to be callable")
        return self.return_type(value)  # pylint: disable=not-callable

    @abstractmethod
    def validate(self, value):
        """Validates value based on various relevant criteria"""


class MyProperty(Property):
    """Copy of AsInstanceOf"""

    def __init__(self, fget=None, fset=None, fdel=None, doc=None):
        super().__init__(fget, fset, fdel, doc)

    def validate(self, value):
        pass
