"""Module for testing the ArcPVA class functionality"""

import math

import numpy as np
import pytest

from pymesh import Point, Vector3D, ArcPVA


@pytest.fixture
def point() -> Point:
    return Point(1, 0, 0)


@pytest.fixture
def axis() -> Vector3D:
    return Vector3D(Point(0, 0, 0), Point(0, 0, 1))


@pytest.fixture
def angle() -> float:
    return math.pi / 2


@pytest.fixture
def curve1(point, axis, angle) -> ArcPVA:
    return ArcPVA(point, axis, angle)


@pytest.fixture
def curve1_moved(dx, dy, dz):
    point = Point(1 + dx, 0 + dy, 0 + dz)
    axis = Vector3D(Point(0 + dx, 0 + dy, 0 + dz), Point(0 + dx, 0 + dy, 1 + dz))
    angle = math.pi / 2
    return ArcPVA(point, axis, angle)


@pytest.fixture
def curve1_rotated():
    point = Point(0, 1, 0)
    axis = Vector3D(Point(0, 0, 0), Point(0, 0, 1))
    angle = math.pi / 2
    return ArcPVA(point, axis, angle)


def test_init_invalid() -> None:
    with pytest.raises(TypeError):
        ArcPVA(Point(0, 0, 0), "point2", None)


def test_eq(curve1) -> None:
    assert curve1 == curve1


def test_ne(curve1, curve1_moved) -> None:
    assert curve1 != curve1_moved


def test_repr(curve1) -> None:
    print("Curve.__repr__ =", f"{curve1!r}")
    assert (
        f"{curve1!r}"
        == "ArcPVA(start=Point(x=1.00, y=0.00, z=0.00), axis=Vector3D(start=Point(x=0.00, y=0.00, z=0.00), end=Point(x=0.00, y=0.00, z=1.00)), angle=1.57)"
    )


def test_start(point: Point, axis: Vector3D, angle: float) -> None:
    curve = ArcPVA(point, axis, angle)
    assert isinstance(curve.start, Point)
    assert curve.start == point


def test_end(curve1: ArcPVA) -> None:
    path_fn = curve1.get_path()
    end_xyz = path_fn(1)
    assert isinstance(curve1.end, Point)
    assert np.all(curve1.end.xyz == end_xyz)


def test_axis(point: Point, axis: Vector3D, angle: float) -> None:
    curve = ArcPVA(point, axis, angle)
    assert isinstance(curve.axis, Vector3D)
    assert curve.axis == axis


def test_angle(point: Point, axis: Vector3D, angle: float) -> None:
    curve = ArcPVA(point, axis, angle)
    assert isinstance(curve.angle, float)
    assert curve.angle == angle


def test_radius(curve1: ArcPVA) -> None:
    assert isinstance(curve1.radius, float)
    assert curve1.radius == 1.0


def test_length(curve1: ArcPVA) -> None:
    assert isinstance(curve1.length, float)
    assert curve1.length == 1.0 * 90.0 * math.pi / 180.0


def test_path(
    assert_curve_path_rounded, point: Point, axis: Vector3D, angle: float
) -> None:
    decimals = 4
    curve1 = ArcPVA(point, axis, angle)
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


def test_rotate(assert_rotate, curve1, curve1_rotated, axis, angle) -> None:
    print(curve1, curve1_rotated)
    assert_rotate(curve1, curve1_rotated, axis, angle)


def test_mirror() -> None:
    axis = Vector3D(Point(0, 0, 0), Point(0, 0, 1))
    assert ArcPVA(Point(-1, 0, 0), axis, -math.pi / 2).mirror(1, 0, 0) == ArcPVA(
        Point(0, 0, 0), axis, math.pi / 2
    )
