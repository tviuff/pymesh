"""Module initializer (constructor)"""

import math
from abc import ABC, abstractmethod

def flip_exp(exp, flip_direction:bool):
    """Flips 'exp' to '1.0 - exp' if flip_direction is True"""
    if not isinstance(flip_direction, bool):
        raise TypeError("flip_direction must be of type 'bool'")
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
    def get_fn(self, flip_direction:bool):
        """Returns distribution function which takes a single float from 0 to 1
        and returns a float between 0 and 1 according to the distribution type.
        """


class LinearDistribution(DistributionMethod):
    """Linear path distribution class"""

    def __init__(self, flip_direction:bool=False):
        super().__init__(flip_direction=flip_direction)

    def get_fn(self):
        flip = True if self.flip_direction else False # breaks ref to self
        def fn(u:int|float, flip_direction:bool=flip) -> float:
            if not isinstance(u, (int, float)):
                raise TypeError("u must be of type 'int' or 'float'")
            if not isinstance(flip_direction, bool):
                raise TypeError("flip_direction mus be of type 'bool'")
            return u
        return fn


class CosineDistribution(DistributionMethod):
    """Cosine path distribution class"""

    def __init__(self, flip_direction:bool=False):
        super().__init__(flip_direction=flip_direction)

    def get_fn(self):
        flip = True if self.flip_direction else False # breaks ref to self
        def fn(u:int|float, flip_direction:bool=flip) -> float:
            if not isinstance(u, (int, float)):
                raise TypeError("u must be of type 'int' or 'float'")
            if not isinstance(flip_direction, bool):
                raise TypeError("flip_direction mus be of type 'bool'")
            if flip_direction:
                u = u + 1.0
            exp = math.cos((u - 1.0)*math.pi/2)
            return flip_exp(exp, flip_direction)
        return fn


class ExponentialDistribution(DistributionMethod):
    """Exponential path distribution class"""

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

    def get_fn(self):
        flip = True if self.flip_direction else False # breaks ref to self
        def fn(u:int|float, flip_direction:bool=flip) -> float:
            if not isinstance(u, (int, float)):
                raise TypeError("u must be of type 'int' or 'float'")
            if not isinstance(flip_direction, bool):
                raise TypeError("flip_direction mus be of type 'bool'")
            if flip_direction:
                u = 1.0 - u
            exp = (math.exp(self.ratio*u) - 1.0) / (math.exp(self.ratio*1.0) - 1.0)
            return flip_exp(exp, flip_direction)
        return fn


class PowerDistribution(DistributionMethod):
    """Power path distribution class"""

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

    def get_fn(self):
        flip = True if self.flip_direction else False # breaks ref to self
        def fn(u:int|float, flip_direction:bool=flip) -> float:
            if not isinstance(u, (int, float)):
                raise TypeError("u must be of type 'int' or 'float'")
            if not isinstance(flip_direction, bool):
                raise TypeError("flip_direction mus be of type 'bool'")
            if flip_direction:
                u = 1.0 - u
            exp = u**self.power
            return flip_exp(exp, flip_direction)
        return fn
