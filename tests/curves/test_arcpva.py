"""Module for testing the Point class functionality"""

import math

import numpy as np
from numpy import ndarray
import pytest

from pygdf import Point, Vector3D, ArcPVA


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
def curve(point: Point, axis: Vector3D, angle: float) -> ArcPVA:
    return ArcPVA(point, axis, angle)


def test_init(point: Point, axis: Vector3D, angle: float) -> None:
    ArcPVA(point, axis, angle)


def test_init_invalid() -> None:
    with pytest.raises(TypeError):
        ArcPVA(Point(0, 0, 0), "point2", None)


def test_eq(curve: ArcPVA) -> None:
    assert curve == curve


def test_start(point: Point, axis: Vector3D, angle: float) -> None:
    curve = ArcPVA(point, axis, angle)
    assert isinstance(curve.start, np.ndarray)
    assert np.all(curve.start == point.xyz)


def test_point_start(point: Point, axis: Vector3D, angle: float) -> None:
    curve = ArcPVA(point, axis, angle)
    assert isinstance(curve.point_start, Point)
    assert curve.point_start == point


def test_point_end(curve: ArcPVA) -> None:
    path_fn = curve.get_path_fn()
    xyz = path_fn(1)
    point_end = Point(xyz[0], xyz[1], xyz[2])
    assert isinstance(curve.point_end, Point)
    assert curve.point_end == point_end


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


def test_radius(curve: ArcPVA) -> None:
    assert isinstance(curve.radius, float)
    assert curve.radius == 1.0


def test_length(curve: ArcPVA) -> None:
    assert isinstance(curve.length, float)
    assert curve.length == 1.0 * 90.0 * math.pi / 180.0


def test_path(
    assert_rounded_path_xyz, point: Point, axis: Vector3D, angle: float
) -> None:
    decimals = 4
    curve1 = ArcPVA(point, axis, angle)
    assert_rounded_path_xyz(curve1, 0, point.xyz, decimals)
    assert_rounded_path_xyz(curve1, 1, Point(0, 1, 0).xyz, decimals)
    assert_rounded_path_xyz(curve1, -1, point.xyz, decimals)
    assert_rounded_path_xyz(
        curve1,
        0.5,
        np.array([1 / np.sqrt(2), 1 / np.sqrt(2), 0]),
        decimals,
    )
    assert_rounded_path_xyz(
        curve1,
        -0.5,
        np.array([1 / np.sqrt(2), 1 / np.sqrt(2), 0]),
        decimals,
    )
