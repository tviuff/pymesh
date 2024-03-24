# conftest.py

import pytest
import numpy as np
from numpy import ndarray

from pygdf import Point, Line
from pygdf.curves.curve import Curve


@pytest.fixture
def dx() -> int:
    return 0


@pytest.fixture
def dy() -> float:
    return -3.0


@pytest.fixture
def dz() -> float:
    return 4.0


@pytest.fixture
def point1() -> Point:
    return Point(0, 0, 0)


@pytest.fixture
def point2(dx: int | float, dy: int | float, dz: int | float) -> Point:
    return Point(dx, dy, dz)


@pytest.fixture
def line1(point1: Point, point2: Point) -> Line:
    return Line(point1, point2)


@pytest.fixture
def assert_rounded_path_xyz():
    def fn(curve: Curve, u: int | float, xyz: ndarray, decimals: int = 0) -> None:
        result = np.round(curve.path(u), decimals=decimals)
        expected = np.round(xyz, decimals=decimals)
        assert np.all(result == expected)

    return fn
