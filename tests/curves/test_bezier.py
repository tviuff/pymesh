"""Module for testing the Bezier class functionality"""

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


@pytest.fixture
def curve1_moved(dx, dy, dz):
    p0 = Point(0 + dx, 0 + dy, 0 + dz)
    p1 = Point(1 + dx, 0 + dy, 0 + dz)
    p2 = Point(2 + dx, 0 + dy, 0 + dz)
    return Bezier([p0, p1, p2])


@pytest.fixture
def curve1_rotated():
    return Bezier([Point(0, 0, 0), Point(0, 1, 0), Point(0, 2, 0)])


def test_init_invalid() -> None:
    with pytest.raises(TypeError):
        Bezier([Point(0, 0, 0), "angle"])


@pytest.mark.skip(reason="Test not implemented")
def test_eq(curve1) -> None:
    assert curve1 == curve1


def test_repr(curve1) -> None:
    print("Curve.__repr__ =", f"{curve1!r}")
    assert (
        f"{curve1!r}"
        == "Bezier(points=[Point(x=0.00, y=0.00, z=0.00), "
        + "Point(x=1.00, y=0.00, z=0.00), Point(x=2.00, y=0.00, z=0.00)])"
    )


def test_start(curve1, points) -> None:
    assert isinstance(curve1.start, Point)
    assert curve1.start == points[0]


def test_end(curve1, points) -> None:
    assert isinstance(curve1.end, Point)
    assert curve1.end == points[-1]


def test_length(curve1) -> None:
    assert isinstance(curve1.length, float)
    assert curve1.length == 2.0


def test_path(assert_curve_path_rounded, points) -> None:
    DECIMALS = 4
    curve = Bezier(points)
    assert_curve_path_rounded(curve, 0.0, False, points[0].xyz, DECIMALS)
    assert_curve_path_rounded(curve, 0.5, False, points[1].xyz, DECIMALS)
    assert_curve_path_rounded(curve, 1.0, False, points[2].xyz, DECIMALS)


def test_copy(assert_copy, curve1) -> None:
    assert_copy(curve1)


def test_move(assert_move, curve1, curve1_moved, dx, dy, dz) -> None:
    assert_move(curve1, curve1_moved, dx, dy, dz)


def test_rotate(assert_rotate, curve1, curve1_rotated, angle) -> None:
    assert_rotate(curve1, curve1_rotated, a=0, b=0, c=1, angle=angle)
