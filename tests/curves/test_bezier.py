"""Module for testing the Bezier class functionality"""

import math

import numpy as np
import pytest

from pymesh import Point, Bezier


@pytest.fixture
def points() -> list[Point]:
    p0 = Point(0, 0, 0)
    p1 = Point(1, 0, 0)
    p2 = Point(2, 0, 0)
    return [p0, p1, p2]


@pytest.fixture
def curve1(points) -> Bezier:
    return Bezier(points)


def test_path(assert_curve_path_rounded, points) -> None:
    decimals = 4
    curve = Bezier(points)
    assert_curve_path_rounded(curve, 0, False, points[0].xyz, decimals)
    assert_curve_path_rounded(curve, 1, False, points[-1].xyz, decimals)
