"""Module initializer (constructor)"""

import math
from abc import ABC, abstractmethod

from gdf.descriptors import AsNumber

class MeshDistribution(ABC):
    """Abstract mesh distribution class"""

    def __init__(self, flip_direction:bool=False):
        self.flip_direction = flip_direction

    def __str__(self) -> str:
        return self.__class__.__name__

    @property
    def flip_direction(self) -> bool:
        return self._flip_direction

    @flip_direction.setter
    def flip_direction(self, value) -> None:
        if not isinstance(value, bool):
            raise TypeError("flip_direction must be of type 'bool'")
        self._flip_direction = value

    @abstractmethod
    def get_dist_fn(self, flip_direction:bool):
        """Returns distribution function which takes a single float from 0 to 1
        and returns a float between 0 and 1 according to the distribution type.
        """

    @staticmethod
    def flip_exp(exp, flip_direction:bool):
        """Flips 'exp' to '1.0 - exp' if flip_direction is True"""
        if not flip_direction:
            return exp
        return 1.0 - exp

    @staticmethod
    def validate_fn_input(u:int|float, flip_direction:bool) -> float:
        """Validates type of inputs u and flip_direction"""
        if not isinstance(flip_direction, bool):
            raise TypeError("flip_direction mus be of type 'bool'")
        if not isinstance(u, (int, float)):
            raise TypeError("u must be of type 'int' or 'float'")
        if isinstance(u, int):
            u = float(u)
        if u < 0 or u > 1:
            raise ValueError("u must be a value between 0 and 1")
        if flip_direction:
            u = 1.0 - u
        return u


class LinearDistribution(MeshDistribution):
    """Linear path distribution class
    expression: fn(u) = u
    """

    def __init__(self, flip_direction:bool=False):
        super().__init__(flip_direction=flip_direction)

    def get_dist_fn(self):
        flip = True if self.flip_direction else False # breaks ref to self
        def fn(u:int|float, flip_direction:bool=flip) -> float:
            u = self.validate_fn_input(u=u, flip_direction=flip_direction)
            exp = u
            return self.flip_exp(exp, flip_direction)
        return fn


class CosineDistribution(MeshDistribution):
    """Cosine path distribution class
    expression: fn(u) = cos[(u-1)*pi/2]
    """

    def __init__(self, flip_direction:bool=False):
        super().__init__(flip_direction=flip_direction)

    def get_dist_fn(self):
        flip = True if self.flip_direction else False # breaks ref to self
        def fn(u:int|float, flip_direction:bool=flip) -> float:
            u = self.validate_fn_input(u=u, flip_direction=flip_direction)
            exp = math.cos((u - 1.0)*math.pi/2)
            return self.flip_exp(exp, flip_direction)
        return fn


class ExponentialDistribution(MeshDistribution):
    """Exponential path distribution class
    expression: fn(u) = exp[ratio*u]
    """

    ratio = AsNumber(return_type=float)

    def __init__(self, ratio:int|float=1.0, flip_direction:bool=False):
        super().__init__(flip_direction=flip_direction)
        self.ratio = ratio

    def get_dist_fn(self):
        flip = True if self.flip_direction else False # breaks ref to self
        def fn(u:int|float, flip_direction:bool=flip) -> float:
            u = self.validate_fn_input(u=u, flip_direction=flip_direction)
            exp = (math.exp(self.ratio*u) - 1.0) / (math.exp(self.ratio*1.0) - 1.0)
            return self.flip_exp(exp, flip_direction)
        return fn


class PowerDistribution(MeshDistribution):
    """Power path distribution class
    expression: fn(u) = u**power
    """

    power = AsNumber(return_type=float)

    def __init__(self, power:int|float=1.0, flip_direction:bool=False):
        super().__init__(flip_direction=flip_direction)
        self.power = power

    def get_dist_fn(self):
        flip = True if self.flip_direction else False # breaks ref to self
        def fn(u:int|float, flip_direction:bool=flip) -> float:
            u = self.validate_fn_input(u=u, flip_direction=flip_direction)
            exp = u**self.power
            return self.flip_exp(exp, flip_direction)
        return fn
