"""Module initializer (constructor)"""

import math
from abc import ABC, abstractmethod


def flip_exp(exp, flip):
    """flips distribution direction from 0-1 to 1-0"""
    if not flip:
        return exp
    return 1 - exp


class DistributionMethod(ABC):
    """Abstract path distribution class"""

    def __init__(self, flip_dir:bool=False):
        self.flip_dir = flip_dir

    def __str__(self) -> str:
        return self.__class__.__name__

    @property
    def flip_dir(self) -> bool:
        return self._flip_dir

    @flip_dir.setter
    def flip_dir(self, value) -> None:
        if not isinstance(value, bool):
            raise TypeError("flip_dir must be of type 'bool'")
        self._flip_dir = value

    @abstractmethod
    def get_fn(self):
        """Returns distribution function whoch takes a single float from 0 to 1
        and returns a vlue between 0 and 1 according to the distribution type.
        If flip_dir = True then the return value u becomes 1 - u."""


class LinearDistribution(DistributionMethod):
    """Linear path distribution class"""

    def __init__(self, flip_dir:bool=False):
        super().__init__(flip_dir=flip_dir)

    def get_fn(self):
        def fn(u:float) -> float:
            exp = u
            return flip_exp(exp, self.flip_dir)
        return fn


class CosineDistribution(DistributionMethod):
    """Cosine path distribution class"""

    def __init__(self, flip_dir:bool=False):
        super().__init__(flip_dir=flip_dir)

    def get_fn(self):
        def fn(u:float) -> float:
            exp = math.cos((u - 1)*math.pi/2)
            return flip_exp(exp, self.flip_dir)
        return fn


class ExponentialDistribution(DistributionMethod):
    """Exponential path distribution class"""

    def __init__(self, flip_dir:bool=False, ratio:int|float=1):
        super().__init__(flip_dir=flip_dir)
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
        def fn(u:float) -> float:
            exp = (math.exp(self.ratio*u) - 1) / (math.exp(self.ratio*1) - 1)
            return flip_exp(exp, self.flip_dir)
        return fn


class PowerDistribution(DistributionMethod):
    """Power path distribution class"""

    def __init__(self, flip_dir:bool=False, power:int|float=1):
        super().__init__(flip_dir=flip_dir)
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
        def fn(u:float) -> float:
            exp = u**self.power
            return flip_exp(exp, self.flip_dir)
        return fn
