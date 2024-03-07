"""https://www.youtube.com/watch?v=DpMGEhwuuyA"""

from typing import Protocol
import math

class DistMethod(Protocol):
    """Abstract path distribution class"""
    def function(self):
        """Returns a path distribution function"""

class Linear(DistMethod):
    """Linear path distribution class"""
    def function(self):
        return lambda x: x

class CosineBoth(DistMethod):
    """Cosine path distribution class"""
    def function(self):
        return lambda u: math.cos((1 - u)*math.pi)/2 + 0.5

class CosineEnd1(DistMethod):
    """Cosine path distribution class"""
    def function(self):
        return lambda u: 1 - math.cos(u*math.pi/2)

class CosineEnd2(DistMethod):
    """Cosine path distribution class"""
    def function(self):
        return lambda u: math.cos((u - 1)*math.pi/2)

class CMesher:
    def __init__(self, dist_method:DistMethod=Linear()):
        self.dist_method = dist_method
    def get_dist_func(self):
        return self.dist_method.function()
