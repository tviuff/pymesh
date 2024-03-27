"""Module for testing the Point class functionality"""

import math

import numpy as np
from numpy import ndarray
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


def test_init(point, axis, angle) -> None:
    ArcPVA(point, axis, angle)


def test_init_invalid() -> None:
    with pytest.raises(TypeError):
        ArcPVA(Point(0, 0, 0), "point2", None)


def test_eq(curve1: ArcPVA) -> None:
    assert curve1 == curve1


def test_ne(curve1: ArcPVA) -> None:
    assert curve1 != curve1


def test_repr(curve1, point, axis, angle) -> None:
    print("Curve.__repr__ =", f"{curve1!r}")
    assert (
        f"{curve1!r}"
        == "ArcPVA(start=Point(x=1.00, y=0.00, z=0.00), axis=Vector3D(dx=0.00, dy=0.00, dz=1.00), angle=1.57)"
    )


def test_start(point: Point, axis: Vector3D, angle: float) -> None:
    curve = ArcPVA(point, axis, angle)
    assert isinstance(curve.start, np.ndarray)
    assert np.all(curve.start == point.xyz)


def test_end(curve1: ArcPVA) -> None:
    path_fn = curve1.get_path()
    end = path_fn(1)
    assert isinstance(curve1.end, np.ndarray)
    assert np.all(curve1.end == end)


def test_start(point: Point, axis: Vector3D, angle: float) -> None:
    curve = ArcPVA(point, axis, angle)
    assert isinstance(curve.start, ndarray)
    assert np.all(curve.start == point.xyz)


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
