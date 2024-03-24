"""Module for testing the Point class functionality"""

import math

import numpy as np
from numpy import ndarray
import pytest

from pygdf import Point, Arc3P


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
def curve(point1: Point, point2: Point, point3: Point) -> Arc3P:
    return Arc3P(point1, point2, point3)


def test_init(point1: Point, point2: Point, point3: Point) -> None:
    Arc3P(point1, point2, point3)


def test_init_invalid() -> None:
    with pytest.raises(TypeError):
        Arc3P(Point(0, 0, 0), "point2", None)


def test_eq(curve: Arc3P) -> None:
    # ! redundant test..
    assert curve == curve


def test_centre(point1: Point, point2: Point, point3: Point) -> None:
    curve1 = Arc3P(point1, point2, point3)
    assert isinstance(curve1.centre, ndarray)
    assert np.all(curve1.centre == point1.xyz)


def test_start(point1: Point, point2: Point, point3: Point) -> None:
    curve1 = Arc3P(point1, point2, point3)
    assert isinstance(curve1.start, ndarray)
    assert np.all(curve1.start == point2.xyz)


def test_end(point1: Point, point2: Point, point3: Point) -> None:
    curve1 = Arc3P(point1, point2, point3)
    assert isinstance(curve1.end, ndarray)
    assert np.all(curve1.end == point3.xyz)


def test_radius(curve: Arc3P) -> None:
    assert isinstance(curve.radius, float)
    assert curve.radius == 1.0


def test_length(curve: Arc3P) -> None:
    assert isinstance(curve.length, float)
    assert curve.length == 1.0 * 90.0 * math.pi / 180.0
    curve.inverse_sector = True
    assert curve.length == 1.0 * (360.0 - 90.0) * math.pi / 180.0


def test_angle(curve: Arc3P) -> None:
    assert isinstance(curve.angle, float)
    assert curve.angle == 90.0 * math.pi / 180.0
    curve.inverse_sector = True
    assert curve.angle == (360.0 - 90.0) * math.pi / 180.0


def test_cross_product(point1: Point, point2: Point, point3: Point) -> None:
    curve1 = Arc3P(point1, point2, point3)
    assert isinstance(curve1.cross_product, ndarray)  #! should be Vector3D
    cross_product_calc = np.cross(point2.xyz - point1.xyz, point3.xyz - point1.xyz)
    assert np.all(curve1.cross_product == cross_product_calc)
    curve1.inverse_sector = True
    assert np.all(curve1.cross_product == -cross_product_calc)


def test_plane_unit_normal(point1: Point, point2: Point, point3: Point) -> None:
    curve1 = Arc3P(point1, point2, point3)
    assert isinstance(curve1.plane_unit_normal, ndarray)  #! should be Vector3D
    calc_cross_product = np.cross(point2.xyz - point1.xyz, point3.xyz - point1.xyz)
    calc_plane_unit_normal = calc_cross_product / np.sqrt(np.sum(calc_cross_product**2))
    assert np.all(curve1.plane_unit_normal == calc_plane_unit_normal)
    curve1.inverse_sector = True
    assert np.all(curve1.plane_unit_normal == -calc_plane_unit_normal)


def test_path(
    assert_rounded_path_xyz, point1: Point, point2: Point, point3: Point
) -> None:
    decimals = 4
    curve1 = Arc3P(point1, point2, point3)
    assert_rounded_path_xyz(curve1, 0, point2.xyz, decimals)
    assert_rounded_path_xyz(curve1, 1, point3.xyz, decimals)
    assert_rounded_path_xyz(curve1, -1, point2.xyz, decimals)
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
