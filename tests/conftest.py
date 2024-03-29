# conftest.py

import math

import pytest
import numpy as np

from pymesh import Point, Vector3D, Line


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
def axis() -> Vector3D:
    return Vector3D(Point(0, 0, 0), Point(0, 0, 1))


@pytest.fixture
def angle() -> float:
    return 90 * math.pi / 180


@pytest.fixture
def p00() -> Point:
    return Point(0, 0, 0)


@pytest.fixture
def p01() -> Point:
    return Point(0, 1, 0)


@pytest.fixture
def p10() -> Point:
    return Point(1, 0, 0)


@pytest.fixture
def p11() -> Point:
    return Point(1, 1, 0)


@pytest.fixture
def point1() -> Point:
    return Point(0, 0, 0)


@pytest.fixture
def point2(dx, dy, dz):
    return Point(dx, dy, dz)


@pytest.fixture
def point1_moved(dx, dy, dz) -> Point:
    return Point(dx, dy, dz)


@pytest.fixture
def point2_moved(dx, dy, dz):
    return Point(2 * dx, 2 * dy, 2 * dz)


@pytest.fixture
def point1_rotated(point1, axis, angle) -> Point:
    point = point1.copy()
    point.rotate(axis, angle)
    return point


@pytest.fixture
def point2_rotated(point2, axis, angle) -> Point:
    point = point2.copy()
    point.rotate(axis, angle)
    return point


@pytest.fixture
def line1(point1, point2) -> Line:
    return Line(point1, point2)


@pytest.fixture
def line1_moved(point1_moved, point2_moved) -> Line:
    return Line(point1_moved, point2_moved)


@pytest.fixture
def line1_rotated(point1_rotated, point2_rotated) -> Line:
    print(point1_rotated, point2_rotated)
    return Line(point1_rotated, point2_rotated)


@pytest.fixture
def line2(point1, point2) -> Line:
    return Line(point2, point1)


@pytest.fixture
def assert_copy():

    def func(old, dx=1, dy=1, dz=1):
        new = old.copy()
        new.move(dx, dy, dz)
        assert new != old, "They both still reference the same data"

    return func


@pytest.fixture
def assert_move():

    def func(self, other, dx=1, dy=1, dz=1):
        self.move(dx, dy, dz)
        assert self == other, "They are not the same, check both .move() and other"

    return func


@pytest.fixture
def assert_rotate():

    def func(
        self,
        other,
        axis=Vector3D(Point(0, 0, 0), Point(0, 0, 1)),
        angle=90 * math.pi / 180,
    ):
        self.rotate(axis, angle)
        assert (
            self == other
        ), "They are not the same, check both self.rotate() and other"

    return func


DECIMALS = 10


@pytest.fixture
def assert_curve_path_rounded():

    def fn(curve, u, flip, xyz, decimals=DECIMALS) -> None:
        result = np.round(curve.path(u, flip), decimals=decimals)
        expected = np.round(xyz, decimals=decimals)
        assert np.all(result == expected)

    return fn


@pytest.fixture
def test_surface_path():
    """Works for all surfaces as long as they generate a plane surface"""

    def func(surface, p00, p01, p10, p11, decimals=DECIMALS):

        def assert_point(surf, u, w, uflip, wflip, point, d=decimals):
            result = np.round(surf.path(u, w, uflip, wflip), decimals=d)
            expected = np.round(point.xyz, decimals=d)
            assert np.all(result == expected)

        # corner p00
        assert_point(surface, 0, 0, False, False, p00)
        assert_point(surface, 1, 1, True, True, p00)
        assert_point(surface, 0, 1, False, True, p00)
        assert_point(surface, 1, 0, True, False, p00)
        # corner p01
        assert_point(surface, 0, 1, False, False, p01)
        assert_point(surface, 1, 0, True, True, p01)
        assert_point(surface, 0, 0, False, True, p01)
        assert_point(surface, 1, 1, True, False, p01)
        # corner p10
        assert_point(surface, 1, 0, False, False, p10)
        assert_point(surface, 0, 1, True, True, p10)
        assert_point(surface, 1, 1, False, True, p10)
        assert_point(surface, 0, 0, True, False, p10)
        # corner p11
        assert_point(surface, 1, 1, False, False, p11)
        assert_point(surface, 0, 0, True, True, p11)
        assert_point(surface, 1, 0, False, True, p11)
        assert_point(surface, 0, 1, True, False, p11)

    return func
