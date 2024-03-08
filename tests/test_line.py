"""Module for testing the Point class functionality"""

import unittest

import numpy as np

from mesh_generator.point import Point
from mesh_generator.curves import Line
from mesh_generator.mesh import Linear

class TestLine(unittest.TestCase):

    def setUp(self):
        point1 = Point(0, 0, 0)
        point2 = Point(2, 0, 0)
        line1 = Line(point1, point2)
        path_fn = line1.get_path_fn()
        self.path_xyz = path_fn(num_points=3, dist_method=Linear)

    def tearDown(self):
        pass

    def test_line(self):
        self.assertEqual(
            (self.path_xyz == np.array([
                [0.0, 0.0, 0.0],
                [1.0, 0.0, 0.0],
                [2.0, 0.0, 0.0]]
            )).all(),
            True
        )

if __name__ == '__main__':
    unittest.main()
