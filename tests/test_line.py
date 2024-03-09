"""Module for testing the Point class functionality"""

import numpy as np
import pytest

from gdfgen.point import Point
from gdfgen.curves import Line
from gdfgen.mesh import Linear

class TestLine:

    def test_get_path_fn(self):

        path_fn = Line(Point(0, 0, 0), Point(2, 0, 0)).get_path_fn()
        path_xyz = path_fn(num_points=3, dist_method=Linear)

        assert (
            path_xyz == np.array([
                [0.0, 0.0, 0.0],
                [1.0, 0.0, 0.0],
                [2.0, 0.0, 0.0]
            ])
        ).all()
