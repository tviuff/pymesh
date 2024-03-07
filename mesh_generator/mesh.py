"""Module with project helper functions related to mesh generation
"""

# MESH ALT2 !!!!

import math
from typing import Final

from .exceptions import NotFoundError

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
        "function": lambda u: math.cos((1 - u)*math.pi)/2 + 0.5,
    },
    "cosine_end1": {
        "description": "increasingly more closely spaced at end1",
        "has_optional_args": False,
        "function": lambda u: 1 - math.cos(u*math.pi/2)
    },
    "cosine_end2": {
        "description": "increasingly more closely spaced at end2",
        "has_optional_args": False,
        "function": lambda u: math.cos((u - 1)*math.pi/2)
    },
}

class CurveMesher:
    """Mesher class used for generating mesh points along curves
    """

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

    def get_mesh_distribution_function(self, option:str=None):
        """Returns selected mesh distribution function.
        """
        option = option or DEFAULT_OPTION
        if option not in MESH_DISTRIBUTION_OPTIONS:
            print(f"'{option}' is not a valid option, defaulting to '{DEFAULT_OPTION}'")
            option = DEFAULT_OPTION
        return MESH_DISTRIBUTION_OPTIONS[option]["function"]

    def print_mesh_dist_option_list(self):
        """Prints indented list of mesh distribution options with corresponding descriptions.
        """
        print("Mesh distribution options and their corresponding descriptions:")
        for key, nested_dict in MESH_DISTRIBUTION_OPTIONS.items():
            print(f"    {key}: {nested_dict["description"]}")


class SurfaceMesher:
    """Mesher class used for generating surface mesh points and panels
    """

    def __init__(self):
        self._mesh_points = None
        self._panels = None

    def generate_panels(self):
        """Generates panels from surface mesh"""
        if self._mesh_points is None:
            # BUG: raise error into a try-except block where mesh points will be generated.
            raise NotFoundError("Surface mesh points not yet generated.")
        panels = []
        mp = self._mesh_points
        for j in range(0, mp.shape[2]-1):
            for i in range(0, mp.shape[1]-1):
                xyz1, xyz2, xyz3, xyz4 = mp[:,i,j], mp[:,i+1,j], mp[:,i+1,j+1], mp[:,i,j+1]
                panels.append([xyz1[0], xyz1[1], xyz1[2], 
                               xyz2[0], xyz2[1], xyz2[2], 
                               xyz3[0], xyz3[1], xyz3[2], 
                               xyz4[0], xyz4[1], xyz4[2]])
        self._panels = panels

    def get_mesh_points(self):
        """Returns surface mesh points"""
        return self._mesh_points

    def get_panels(self):
        """Returns surface mesh points"""
        return self._panels
