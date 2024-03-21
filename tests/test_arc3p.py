"""Module for testing the Point class functionality"""

import math

import numpy as np
from numpy import ndarray
import pytest

from gdf import Point, Arc3P

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
def curve(point1:Point, point2:Point, point3:Point) -> Arc3P:
    return Arc3P(point1, point2, point3)

def test_init(point1:Point, point2:Point, point3:Point) -> None:
    Arc3P(point1, point2, point3)

def test_init_invalid() -> None:
    with pytest.raises(TypeError):
        Arc3P(Point(0, 0, 0), "point2", None)

def test_eq(curve:Arc3P) -> None:
    assert curve == curve

def test_point_centre(point1:Point, point2:Point, point3:Point) -> None:
    point_centre = Arc3P(point1, point2, point3).point_centre
    assert isinstance(point_centre, Point)
    assert point_centre == point1

def test_point_start(point1:Point, point2:Point, point3:Point) -> None:
    point_start = Arc3P(point1, point2, point3).point_start
    assert isinstance(point_start, Point)
    assert point_start == point2

def test_point_end(point1:Point, point2:Point, point3:Point) -> None:
    point_end = Arc3P(point1, point2, point3).point_end
    assert isinstance(point_end, Point)
    assert point_end == point3

def test_vector_start(point1:Point, point2:Point, point3:Point) -> None:
    vector_start = Arc3P(point1, point2, point3).vector_start
    assert isinstance(vector_start, ndarray) #! should be Vector3D
    assert (vector_start == point2.xyz - point1.xyz).any()

def test_vector_end(point1:Point, point2:Point, point3:Point) -> None:
    vector_end = Arc3P(point1, point2, point3).vector_end
    assert isinstance(vector_end, ndarray) #! should be Vector3D
    assert (vector_end == point3.xyz - point1.xyz).any()

def test_radius(curve:Arc3P) -> None:
    assert isinstance(curve.radius, float)
    assert curve.radius == 1.0

def test_length(curve:Arc3P) -> None:
    assert isinstance(curve.length, float)
    assert curve.length == 1.0 * 90.0 * math.pi/180.0
    curve.flipped_dir = True
    assert curve.length == 1.0 * (360.0 - 90.0) * math.pi/180.0

def test_angle(curve:Arc3P) -> None:
    assert isinstance(curve.angle, float)
    assert curve.angle == 90.0 * math.pi/180.0
    curve.flipped_dir = True
    assert curve.angle == (360.0 - 90.0) * math.pi/180.0

def test_cross_product(point1:Point, point2:Point, point3:Point) -> None:
    curve = Arc3P(point1, point2, point3)
    assert isinstance(curve.cross_product, ndarray) #! should be Vector3D
    cross_product_calc = np.cross(point2.xyz-point1.xyz, point3.xyz-point1.xyz)
    assert (curve.cross_product == cross_product_calc).any()
    curve.flipped_dir = True
    assert (curve.cross_product == -cross_product_calc).any()

def test_plane_unit_normal(point1:Point, point2:Point, point3:Point) -> None:
    curve = Arc3P(point1, point2, point3)
    assert isinstance(curve.plane_unit_normal, ndarray) #! should be Vector3D
    calc_cross_product = np.cross(point2.xyz-point1.xyz, point3.xyz-point1.xyz)
    calc_plane_unit_normal = calc_cross_product / np.sqrt(np.sum(calc_cross_product**2))
    assert (curve.plane_unit_normal == calc_plane_unit_normal).any()
    curve.flipped_dir = True
    assert (curve.plane_unit_normal == -calc_plane_unit_normal).any()

def test_get_path_fn(point1:Point, point2:Point, point3:Point) -> None:
    path_fn = Arc3P(point1, point2, point3).get_path_fn()
    assert (path_fn(0) == point2.xyz).any()
    assert (path_fn(1) == point3.xyz).any()
    assert (path_fn(0, flip_direction=True) == point3.xyz).any()
    assert (path_fn(1, flip_direction=True) == point2.xyz).any()
    assert (path_fn(0.5) == np.array([np.sqrt(2), np.sqrt(2), 0])).any()
    assert (path_fn(0.5, flip_direction=True) == np.array([np.sqrt(2), np.sqrt(2), 0])).any()
