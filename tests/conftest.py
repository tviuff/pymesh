# conftest.py

import pytest

from pygdf import Point, Line


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
def point2(dx: float, dy: float, dz: float) -> Point:
    return Point(dx, dy, dz)


@pytest.fixture
def line1(point1: Point, point2: Point) -> Line:
    return Line(point1, point2)
