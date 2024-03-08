"""Module for testing the Point class functionality"""

import unittest

from gdfgen.point import Point

class TestPoint(unittest.TestCase):

    def setUp(self):
        point1 = Point(0, 0, 0)
        point2 = Point(3, 4, 0)
        self.distance = Point.get_distance(point1, point2)

    def tearDown(self):
        pass

    def test_point(self):
        self.assertEqual(self.distance, 5.0)

if __name__ == '__main__':
    unittest.main()
