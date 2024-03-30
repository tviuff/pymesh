"""Module for testing the Point class functionality"""

import math

import numpy as np
import pytest

from pymesh import Point, Vector3D


def test_init(dx, dy, dz) -> None:
    Point(dx, dy, dz)


def test_init_invalid() -> None:
    with pytest.raises(TypeError):
        Point("x", "y", "z")


def test_eq(point1, point2) -> None:
    assert point1 == point1
    assert point2 == point2


def test_ne(point1, point2) -> None:
    assert point1 != point2


def test_repr(point1) -> None:
    assert f"{point1!r}" == "Point(x=0.00, y=0.00, z=0.00)"


def test_x(point2, dx) -> None:
    x = point2.x
    assert isinstance(x, float)
    assert x == dx


def test_y(point2, dy) -> None:
    y = point2.y
    assert isinstance(y, float)
    assert y == dy


def test_z(point2, dz) -> None:
    z = point2.z
    assert isinstance(z, float)
    assert z == dz


def test_xyz(point2, dx, dy, dz) -> None:
    assert np.all(point2.xyz == np.array([dx, dy, dz]))


def test_get_distance_to(point1, point2, dx, dy, dz) -> None:
    assert point1.get_distance_to(point2) == math.sqrt(dx**2 + dy**2 + dz**2)
    assert point2.get_distance_to(point1) == math.sqrt(dx**2 + dy**2 + dz**2)


def test_get_distance_invalid(point1: Point) -> None:
    with pytest.raises(TypeError):
        point1.get_distance_to("")


def test_create_relative_point(point1, point2, dx, dy, dz) -> None:
    assert point1.create_relative_point(dx, dy, dz) == point2


def test_create_relative_point_invalid(point1: Point) -> None:
    with pytest.raises(TypeError):
        point1.create_relative_point("", "", "")


def test_move(assert_move, point1, point2, dx, dy, dz) -> None:
    assert_move(point1, point2, dx, dy, dz)


def test_copy(assert_copy, point1) -> None:
    assert_copy(point1)


def test_rotate(p00, p10, p01) -> None:
    DECIMALS = 4
    angle = 90 * math.pi / 180
    p10.rotate(Vector3D(p00, Point(0, 0, 1)), angle)
    result = np.round(p10.xyz, decimals=DECIMALS)
    expected = np.round(p01.xyz, decimals=DECIMALS)
    assert np.all(result == expected)


def test_mirror() -> None:
    assert Point(0, 1, 0).mirror(1, 0, 0) == Point(0, 1, 0)
    assert Point(1, 0, 0).mirror(1, 0, 0) == Point(-1, 0, 0)
    assert Point(0, 1, 0).mirror(0, 1, 0) == Point(0, -1, 0)
    assert Point(1, 0, 0).mirror(0, 1, 0) == Point(1, 0, 0)
    assert Point(0, 0, 1).mirror(0, 0, 1) == Point(0, 0, -1)
    assert Point(2, 0, 0).mirror(1, 0, 0, x0=1) == Point(0, 0, 0)
    assert Point(0, 2, 0).mirror(0, 1, 0, y0=1) == Point(0, 0, 0)
    assert Point(0, 0, 3).mirror(0, 0, 1, z0=2) == Point(0, 0, 1)
