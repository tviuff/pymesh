"""Module with curve distibution classes
"""

import math
from typing import Protocol

def flip_exp(exp, flip):
    if not flip:
        return exp
    return 1 - exp

class DistMethod(Protocol):

    def __str__(self) -> str:
        ...

    def get_fn(self, flip_dir:bool):
        ...

class DistLinear:
    """Linear path distribution class"""

    def __str__(self) -> str:
        return self.__class__.__name__

    def get_fn(self, flip_dir:bool):
        def fn(u:float) -> float:
            exp = u
            return flip_exp(exp, flip_dir)
        return fn

class DistCosineBoth:
    """Cosine path distribution class"""

    def __str__(self) -> str:
        return self.__class__.__name__

    def get_fn(self, flip_dir:bool):
        def fn(u:float) -> float:
            exp = math.cos((1 - u)*math.pi)/2 + 0.5
            return flip_exp(exp, flip_dir)
        return fn

class DistCosineEnd1:
    """Cosine path distribution class"""

    def __str__(self) -> str:
        return self.__class__.__name__

    def get_fn(self, flip_dir:bool):
        def fn(u:float) -> float:
            exp = 1 - math.cos(u*math.pi/2)
            return flip_exp(exp, flip_dir)
        return fn

class DistCosineEnd2:
    """Cosine path distribution class"""

    def __str__(self) -> str:
        return self.__class__.__name__

    def get_fn(self, flip_dir:bool):
        def fn(u:float) -> float:
            exp = math.cos((u - 1)*math.pi/2)
            return flip_exp(exp, flip_dir)
        return fn
