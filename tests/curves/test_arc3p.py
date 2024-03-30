"""Module for testing the Point class functionality"""

import math

import numpy as np
from numpy import ndarray
import pytest

from pymesh import Point, Arc3P


@pytest.fixture
def point1() -> Point:
    return Point(0, 0, 0)


@pytest.fixture
def point2() -> Point:
    return Point(1, 0, 0)


@pytest.fixture
def point3() -> Point:
    return Point(0, 1, 0)


@pytest.fixture
def curve1(point1: Point, point2: Point, point3: Point) -> Arc3P:
    return Arc3P(point1, point2, point3)


@pytest.fixture
def curve2(point1: Point, point2: Point, point3: Point) -> Arc3P:
    return Arc3P(point1, point3, point2)


def test_init(point1: Point, point2: Point, point3: Point) -> None:
    Arc3P(point1, point2, point3)


def test_init_invalid() -> None:
    with pytest.raises(TypeError):
        Arc3P(Point(0, 0, 0), "point2", None)


def test_ne(curve1: Arc3P, curve2: Arc3P) -> None:
    assert curve1 != curve2


def test_centre(point1: Point, point2: Point, point3: Point) -> None:
    curve = Arc3P(point1, point2, point3)
    assert isinstance(curve.centre, Point)
    assert np.all(curve.centre == point1)


def test_start(point1: Point, point2: Point, point3: Point) -> None:
    curve = Arc3P(point1, point2, point3)
    assert isinstance(curve.start, Point)
    assert np.all(curve.start == point2)


def test_end(point1: Point, point2: Point, point3: Point) -> None:
    curve = Arc3P(point1, point2, point3)
    assert isinstance(curve.end, Point)
    assert np.all(curve.end == point3)


def test_radius(curve1: Arc3P) -> None:
    assert isinstance(curve1.radius, float)
    assert curve1.radius == 1.0


def test_length(curve1: Arc3P) -> None:
    assert isinstance(curve1.length, float)
    assert curve1.length == 1.0 * 90.0 * math.pi / 180.0
    curve1.inverse_sector = True
    assert curve1.length == 1.0 * (360.0 - 90.0) * math.pi / 180.0


def test_angle(curve1: Arc3P) -> None:
    assert isinstance(curve1.angle, float)
    assert curve1.angle == 90.0 * math.pi / 180.0
    curve1.inverse_sector = True
    assert curve1.angle == (360.0 - 90.0) * math.pi / 180.0


def test_cross_product(point1: Point, point2: Point, point3: Point) -> None:
    curve = Arc3P(point1, point2, point3)
    assert isinstance(curve.cross_product, ndarray)  #! should be Vector3D
    cross_product_calc = np.cross(point2.xyz - point1.xyz, point3.xyz - point1.xyz)
    assert np.all(curve.cross_product == cross_product_calc)
    curve.inverse_sector = True
    assert np.all(curve.cross_product == -cross_product_calc)


def test_plane_unit_normal(point1: Point, point2: Point, point3: Point) -> None:
    curve = Arc3P(point1, point2, point3)
    assert isinstance(curve.plane_unit_normal, ndarray)  #! should be Vector3D
    calc_cross_product = np.cross(point2.xyz - point1.xyz, point3.xyz - point1.xyz)
    calc_plane_unit_normal = calc_cross_product / np.sqrt(np.sum(calc_cross_product**2))
    assert np.all(curve.plane_unit_normal == calc_plane_unit_normal)
    curve.inverse_sector = True
    assert np.all(curve.plane_unit_normal == -calc_plane_unit_normal)


def test_path(
    assert_curve_path_rounded, point1: Point, point2: Point, point3: Point
) -> None:
    decimals = 4
    curve = Arc3P(point1, point2, point3)
    assert_curve_path_rounded(curve, 0, False, point2.xyz, decimals)
    assert_curve_path_rounded(curve, 1, False, point3.xyz, decimals)
    assert_curve_path_rounded(curve, 1, True, point2.xyz, decimals)
    assert_curve_path_rounded(
        curve,
        0.5,
        False,
        np.array([1 / np.sqrt(2), 1 / np.sqrt(2), 0]),
        decimals,
    )
    assert_curve_path_rounded(
        curve,
        0.5,
        True,
        np.array([1 / np.sqrt(2), 1 / np.sqrt(2), 0]),
        decimals,
    )


def test_copy(assert_copy, curve1) -> None:
    assert_copy(curve1)


def test_move(assert_move, curve1, dx, dy, dz) -> None:
    p1 = Point(0 + dx, 0 + dy, 0 + dz)
    p2 = Point(1 + dx, 0 + dy, 0 + dz)
    p3 = Point(0 + dx, 1 + dy, 0 + dz)
    curve1_moved = Arc3P(p1, p2, p3)
    assert_move(curve1, curve1_moved, dx, dy, dz)


def test_rotate(assert_rotate, angle) -> None:
    curve1 = Arc3P(Point(0, 0, 0), Point(1, 0, 0), Point(0, 1, 0))
    curve1_rotated = Arc3P(Point(0, 0, 0), Point(0, 1, 0), Point(-1, 0, 0))
    assert_rotate(curve1, curve1_rotated, a=0, b=0, c=1, angle=angle)


def test_mirror() -> None:
    assert Arc3P(Point(0, 0, 0), Point(-1, 0, 0), Point(0, 1, 0)).mirror(
        1, 0, 0
    ) == Arc3P(Point(0, 0, 0), Point(1, 0, 0), Point(0, 1, 0))
