"""Module for testing the Point class functionality"""

import pytest

from gdfgen.point import Point

class TestPoint:

    def test_get_distance(self):
        distance = Point.get_distance(Point(0, 0, 0), Point(3, 4, 0))
        assert distance == 5.0

    def test_set_relative_to(self):
        point = Point.set_relative_to(Point(0, 0, 0), 1, 2, 3)
        assert point == Point(1, 2, 3)
