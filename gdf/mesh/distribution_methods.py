"""Module initializer (constructor)"""

import math
from abc import ABC, abstractmethod


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


def flip_exp(exp, flip_direction:bool):
    """Flips 'exp' to '1.0 - exp' if flip_direction is True"""
    if not flip_direction:
        return exp
    return 1.0 - exp


class DistributionMethod(ABC):
    """Abstract path distribution class"""

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


class LinearDistribution(DistributionMethod):
    """Linear path distribution class
    expression: fn(u) = u
    """

    def __init__(self, flip_direction:bool=False):
        super().__init__(flip_direction=flip_direction)

    def get_dist_fn(self):
        flip = True if self.flip_direction else False # breaks ref to self
        def fn(u:int|float, flip_direction:bool=flip) -> float:
            u = validate_fn_input(u=u, flip_direction=flip_direction)
            exp = u
            return flip_exp(exp, flip_direction)
        return fn


class CosineDistribution(DistributionMethod):
    """Cosine path distribution class
    expression: fn(u) = cos[(u-1)*pi/2]
    """

    def __init__(self, flip_direction:bool=False):
        super().__init__(flip_direction=flip_direction)

    def get_dist_fn(self):
        flip = True if self.flip_direction else False # breaks ref to self
        def fn(u:int|float, flip_direction:bool=flip) -> float:
            u = validate_fn_input(u=u, flip_direction=flip_direction)
            exp = math.cos((u - 1.0)*math.pi/2)
            return flip_exp(exp, flip_direction)
        return fn


class ExponentialDistribution(DistributionMethod):
    """Exponential path distribution class
    expression: fn(u) = exp[ratio*u]
    """

    def __init__(self, ratio:int|float=1.0, flip_direction:bool=False):
        super().__init__(flip_direction=flip_direction)
        self.ratio = ratio

    @property
    def ratio(self) -> float:
        return self._ratio

    @ratio.setter
    def ratio(self, value) -> None:
        if not isinstance(value, (int, float)):
            raise TypeError("ratio must be of type 'int' or 'float'")
        self._ratio = float(value)

    def get_dist_fn(self):
        flip = True if self.flip_direction else False # breaks ref to self
        def fn(u:int|float, flip_direction:bool=flip) -> float:
            u = validate_fn_input(u=u, flip_direction=flip_direction)
            exp = (math.exp(self.ratio*u) - 1.0) / (math.exp(self.ratio*1.0) - 1.0)
            return flip_exp(exp, flip_direction)
        return fn


class PowerDistribution(DistributionMethod):
    """Power path distribution class
    expression: fn(u) = u**power
    """

    def __init__(self, power:int|float=1.0, flip_direction:bool=False):
        super().__init__(flip_direction=flip_direction)
        self.power = power

    @property
    def power(self) -> float:
        return self._power

    @power.setter
    def power(self, value) -> None:
        if not isinstance(value, (int, float)):
            raise TypeError("power must be of type 'int' or 'float'")
        self._power = float(value)

    def get_dist_fn(self):
        flip = True if self.flip_direction else False # breaks ref to self
        def fn(u:int|float, flip_direction:bool=flip) -> float:
            u = validate_fn_input(u=u, flip_direction=flip_direction)
            exp = u**self.power
            return flip_exp(exp, flip_direction)
        return fn
