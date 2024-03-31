"""Module for testing the ArcPVA class functionality"""

import math

import numpy as np
import pytest

from pymesh import Point, ArcPVA


@pytest.fixture
def point() -> Point:
    return Point(1, 0, 0)


@pytest.fixture
def abc() -> tuple[float]:
    return 0, 0, 1


@pytest.fixture
def angle() -> float:
    return math.pi / 2


@pytest.fixture
def curve1(point, angle, abc) -> ArcPVA:
    a, b, c = abc
    return ArcPVA(point, angle, a, b, c)


@pytest.fixture
def curve1_moved(dx, dy, dz):
    angle = math.pi / 2
    point = Point(1 + dx, 0 + dy, 0 + dz)
    return ArcPVA(point, angle, 0, 0, 1, dx, dy, dz)


@pytest.fixture
def curve1_rotated():
    angle = math.pi / 2
    point = Point(0, 1, 0)
    return ArcPVA(point, angle, 0, 0, 1)


def test_init_invalid() -> None:
    with pytest.raises(TypeError):
        ArcPVA(Point(0, 0, 0), "angle", None, "", "")


@pytest.mark.skip(reason="Test not implemented")
def test_eq(curve1) -> None:
    assert curve1 == curve1


def test_ne(curve1, curve1_moved) -> None:
    assert curve1 != curve1_moved


def test_repr(curve1) -> None:
    print("Curve.__repr__ =", f"{curve1!r}")
    assert (
        f"{curve1!r}"
        == "ArcPVA(start=Point(x=1.00, y=0.00, z=0.00), angle=1.57, a=0.00, b=0.00, c=1.00, x0=0.00, y0=0.00, z0=0.00)"
    )


def test_start(point, angle, abc) -> None:
    a, b, c = abc
    curve = ArcPVA(point, angle, a, b, c)
    assert isinstance(curve.start, Point)
    assert curve.start == point


def test_end(curve1) -> None:
    path_fn = curve1.get_path()
    end_xyz = path_fn(1)
    assert isinstance(curve1.end, Point)
    assert np.all(curve1.end.xyz == end_xyz)


def test_abc_xyz0(point, angle, abc) -> None:
    a, b, c = abc
    curve = ArcPVA(point, angle, a, b, c, 1, 2, 3)
    assert curve.a == a
    assert curve.b == b
    assert curve.c == c
    assert curve.x0 == 1
    assert curve.y0 == 2
    assert curve.z0 == 3


def test_angle(point, angle, abc) -> None:
    a, b, c = abc
    curve = ArcPVA(point, angle, a, b, c)
    assert isinstance(curve.angle, float)
    assert curve.angle == angle


def test_radius(curve1) -> None:
    assert isinstance(curve1.radius, float)
    assert curve1.radius == 1.0


def test_length(curve1) -> None:
    assert isinstance(curve1.length, float)
    assert curve1.length == 1.0 * 90.0 * math.pi / 180.0


def test_path(assert_curve_path_rounded, point, angle, abc) -> None:
    decimals = 4
    a, b, c = abc
    curve1 = ArcPVA(point, angle, a, b, c)
    assert_curve_path_rounded(curve1, 0, False, point.xyz, decimals)
    assert_curve_path_rounded(curve1, 1, False, Point(0, 1, 0).xyz, decimals)
    assert_curve_path_rounded(curve1, 1, True, point.xyz, decimals)
    assert_curve_path_rounded(
        curve1,
        0.5,
        False,
        np.array([1 / np.sqrt(2), 1 / np.sqrt(2), 0]),
        decimals,
    )
    assert_curve_path_rounded(
        curve1,
        0.5,
        True,
        np.array([1 / np.sqrt(2), 1 / np.sqrt(2), 0]),
        decimals,
    )


def test_copy(assert_copy, curve1) -> None:
    assert_copy(curve1)


def test_move(assert_move, curve1, curve1_moved, dx, dy, dz) -> None:
    assert_move(curve1, curve1_moved, dx, dy, dz)


def test_rotate(assert_rotate, curve1, curve1_rotated, angle) -> None:
    assert_rotate(curve1, curve1_rotated, a=0, b=0, c=1, angle=angle)


def test_mirror() -> None:
    assert ArcPVA(Point(-1, 0, 0), -math.pi / 2, 0, 0, 1).mirror(1, 0, 0) == ArcPVA(
        Point(0, 0, 0), math.pi / 2, 0, 0, 1
    )
