# conftest.py

import pytest
import numpy as np

from pymesh import Point, Line


DECIMALS = 4


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
def point3(dx, dy, dz):
    return Point(2 * dx, 2 * dy, 2 * dz)


@pytest.fixture
def line1(point1, point2) -> Line:
    return Line(point1, point2)


@pytest.fixture
def line1_moved(point2, point3) -> Line:
    return Line(point2, point3)


@pytest.fixture
def line2(point1, point2) -> Line:
    return Line(point2, point1)


@pytest.fixture
def assert_curve_path_rounded():

    def fn(curve, u, flip, xyz, decimals=DECIMALS) -> None:
        result = np.round(curve.path(u, flip), decimals=decimals)
        expected = np.round(xyz, decimals=decimals)
        assert np.all(result == expected)

    return fn


@pytest.fixture
def assert_surface_path_rounded():

    def fn(surface, u, w, uflip, wflip, xyz, decimals=DECIMALS) -> None:
        result = np.round(surface.path(u, w, uflip, wflip), decimals=decimals)
        expected = np.round(xyz, decimals=decimals)
        assert np.all(result == expected)

    return fn


@pytest.fixture
def test_surface_path(assert_surface_path_rounded):
    """Works for all surfaces as long as they generate a plane surface"""

    def func(surface, p00, p01, p10, p11, decimals=DECIMALS):

        def assert_point(surf, u, w, uflip, wflip, point, d=decimals):
            assert_surface_path_rounded(surf, u, w, uflip, wflip, point.xyz, d)

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


@pytest.fixture
def assert_move():

    def func(self, other, dx=1, dy=1, dz=1):
        self.move(dx, dy, dz)
        assert self == other, "They are not the same, check both .move() and other"

    return func


@pytest.fixture
def assert_copy():

    def func(old, dx=1, dy=1, dz=1):
        new = old.copy()
        new.move(dx, dy, dz)
        assert new != old, "They both still reference the same data"

    return func
