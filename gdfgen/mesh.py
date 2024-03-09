"""Module with curve distibution classes
"""

import math
from typing import Protocol

class DistributionMethodInstance(Protocol):
    """Abstract path distribution class"""
    def __str__() -> str:
        """Returns string representation of instance"""
    def get_fn():
        """Returns method distribution function"""

class DistributionMethod(DistributionMethodInstance):
    """Parent distribution class"""
    def __str__(self) -> str:
        return self.__class__.__name__

class Linear(DistributionMethod):
    """Linear path distribution class"""
    def get_fn():
        return lambda x: x

class CosineBoth(DistributionMethod):
    """Cosine path distribution class"""
    def get_fn():
        return lambda u: math.cos((1 - u)*math.pi)/2 + 0.5

class CosineEnd1(DistributionMethod):
    """Cosine path distribution class"""
    def get_fn():
        return lambda u: 1 - math.cos(u*math.pi/2)

class CosineEnd2(DistributionMethod):
    """Cosine path distribution class"""
    def get_fn():
        return lambda u: math.cos((u - 1)*math.pi/2)
