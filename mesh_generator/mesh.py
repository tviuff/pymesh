"""Module with project helper functions related to mesh generation
"""

import math
from typing import Final

DEFAULT_NUM_POINTS: Final = 5
DEFAULT_OPTION: Final = "linear"
MESH_DISTRIBUTION_OPTIONS: Final = {
    "linear": {
        "description": "linearly spaced",
        "has_optional_args": False,
        "function": lambda u: u,
    },
    "cosine_both": {
        "description": "increasingly more closely spaced at the ends",
        "has_optional_args": False,
        "function": lambda u: math.cos(math.pi*(1 - u))/2 + 0.5,
    },
    "cosine_end1": {
        "description": "increasingly more closely spaced at end1",
        "has_optional_args": False,
        "function": lambda u: 1 - math.cos(math.pi*u/2)
    },
    "cosine_end2": {
        "description": "increasingly more closely spaced at end2",
        "has_optional_args": False,
        "function": lambda u: math.cos(math.pi*u/2)
    },
}

class Mesher:
    """Mesher class used for generatin mesh points along curves
    """

    def _get_mesh_distribution_function(self, option:str=None):
        """Returns selected mesh distribution function.
        """
        option = option or DEFAULT_OPTION
        if option not in MESH_DISTRIBUTION_OPTIONS:
            print(f"'{option}' is not a valid option, defaulting to '{DEFAULT_OPTION}'")
            option = DEFAULT_OPTION
        return MESH_DISTRIBUTION_OPTIONS[option]["function"]

    def _validate_mesh_num_points(self, num_points:int=DEFAULT_NUM_POINTS):
        """Validates num_point by raising exceptions if not ok
        """
        try:
            if not isinstance(num_points, int):
                raise TypeError("num_points must be of type 'int'.")
            if num_points <= 1:
                raise ValueError("'num_points' must be larger than 1")
        except ValueError as e:
            num_points = DEFAULT_NUM_POINTS
            print(f"{e}, defaulting to '{num_points}'")
        return num_points

    def print_mesh_dist_option_list(self) -> dict:
        """Prints indented list of mesh distribution options with corresponding descriptions.
        """
        print("Mesh distribution options and their corresponding descriptions:")
        for key, nested_dict in MESH_DISTRIBUTION_OPTIONS.items():
            print(f"    {key}: {nested_dict["description"]}")
