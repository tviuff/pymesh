"""Module initializer (constructor)"""

import math
from abc import ABC, abstractmethod


def flip_exp(exp, flip):
    """flips distribution direction from 0-1 to 1-0"""
    if not flip:
        return exp
    return 1 - exp


class DistMethod(ABC):
    """Abstract path distribution class"""

    def __str__(self) -> str:
        return self.__class__.__name__

    @abstractmethod
    def get_fn(self, flip_dir:bool):
        pass


class DistLinear(DistMethod):
    """Linear path distribution class"""

    def get_fn(self, flip_dir:bool):
        def fn(u:float) -> float:
            exp = u
            return flip_exp(exp, flip_dir)
        return fn


class DistCosine(DistMethod):
    """Cosine path distribution class"""

    def get_fn(self, flip_dir:bool):
        def fn(u:float) -> float:
            exp = math.cos((u - 1)*math.pi/2)
            return flip_exp(exp, flip_dir)
        return fn


class DistExp(DistMethod):
    """Exponential path distribution class"""

    def __init__(self, ratio:int|float=1):
        self.ratio = ratio

    @property
    def ratio(self) -> float:
        return self._ratio

    @ratio.setter
    def ratio(self, value) -> None:
        if not isinstance(value, (int, float)):
            raise TypeError("ratio must be of type 'int' or 'float'")
        self._ratio = float(value)

    def get_fn(self, flip_dir:bool):
        def fn(u:float) -> float:
            exp = (math.exp(self.ratio*u) - 1) / (math.exp(self.ratio*1) - 1)
            return flip_exp(exp, flip_dir)
        return fn


class DistPower(DistMethod):
    """Power path distribution class"""

    def __init__(self, power:int|float=1):
        self.power = power

    @property
    def power(self) -> float:
        return self._power

    @power.setter
    def power(self, value) -> None:
        if not isinstance(value, (int, float)):
            raise TypeError("power must be of type 'int' or 'float'")
        self._power = float(value)

    def get_fn(self, flip_dir:bool):
        def fn(u:float) -> float:
            exp = u^self.power
            return flip_exp(exp, flip_dir)
        return fn
