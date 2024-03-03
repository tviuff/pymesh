"""Module with project constants
"""

import math

DEFAULT_DIST_METHOD = "linear"
DIST_METHOD_FUNCTIONS = {
    DEFAULT_DIST_METHOD: lambda u: u,
    "cosine_both": lambda u: math.cos(math.pi*(1 - u))/2 + 0.5,
    "cosine_end1": lambda u: 1 - math.cos(math.pi*u/2),
    "cosine_end2": lambda u: math.cos(math.pi*u/2),
}
