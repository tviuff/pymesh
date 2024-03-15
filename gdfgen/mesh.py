"""Module with curve distibution classes
"""

import math
from abc import ABC, abstractmethod


class DistMethod(ABC):
    """Abstract path distribution class"""

    def __str__(self) -> str:
        return self.__class__.__name__

    @abstractmethod
    def get_fn(self, flip_dir:bool):
        pass


def flip_exp(exp, flip):
    """flips distribution direction from 0-1 to 1-0"""
    if not flip:
        return exp
    return 1 - exp


class DistLinear(DistMethod):
    """Linear path distribution class"""

    def get_fn(self, flip_dir:bool):
        def fn(u:float) -> float:
            exp = u
            return flip_exp(exp, flip_dir)
        return fn


class DistCosineBoth(DistMethod):
    """Cosine path distribution class"""

    def get_fn(self, flip_dir:bool):
        def fn(u:float) -> float:
            exp = math.cos((1 - u)*math.pi)/2 + 0.5
            return flip_exp(exp, flip_dir)
        return fn


class DistCosineEnd1(DistMethod):
    """Cosine path distribution class"""

    def get_fn(self, flip_dir:bool):
        def fn(u:float) -> float:
            exp = 1 - math.cos(u*math.pi/2)
            return flip_exp(exp, flip_dir)
        return fn


class DistCosineEnd2(DistMethod):
    """Cosine path distribution class"""

    def get_fn(self, flip_dir:bool):
        def fn(u:float) -> float:
            exp = math.cos((u - 1)*math.pi/2)
            return flip_exp(exp, flip_dir)
        return fn


class MeshNumber:
    """Mesh number descriptor class used for num_points"""

    def __set_name__(self, owner, name):
        self._name = name

    def __get__(self, instance, owner) -> int:
        return instance.__dict__[self._name]

    def __set__(self, instance, value:int):
        if not isinstance(value, int):
            raise TypeError(f"{self._name} must be of type 'int'")
        instance.__dict__[self._name] = value


class BoundaryDistribution:
    """Boundary dustribution descriptor class used for dist_u0 and others"""

    def __set_name__(self, owner, name):
        self._name = name

    def __get__(self, instance, owner) -> DistMethod:
        return instance.__dict__[self._name]

    def __set__(self, instance, value:DistMethod):
        if not isinstance(value, DistMethod):
            raise TypeError(f"{self._name} must be and instance of a subclass of 'DistMethod'")
        instance.__dict__[self._name] = value
