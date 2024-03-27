"""Module for testing the Point class functionality"""

import math

import numpy as np
import pytest

from pymesh import Point


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


def test_x(point2: Point, dx: float) -> None:
    x = point2.x
    assert isinstance(x, float)
    assert x == dx


def test_y(point2: Point, dy: float) -> None:
    y = point2.y
    assert isinstance(y, float)
    assert y == dy


def test_z(point2: Point, dz: float) -> None:
    z = point2.z
    assert isinstance(z, float)
    assert z == dz


def test_xyz(point2: Point, dx: float, dy: float, dz: float) -> None:
    assert np.all(point2.xyz == np.array([dx, dy, dz]))


def test_get_distance(
    point1: Point, point2: Point, dx: float, dy: float, dz: float
) -> None:
    assert point1.get_distance(point2) == math.sqrt(dx**2 + dy**2 + dz**2)
    assert point2.get_distance(point1) == math.sqrt(dx**2 + dy**2 + dz**2)


def test_get_distance_invalid(point1: Point) -> None:
    with pytest.raises(TypeError):
        point1.get_distance("point")


def test_create_relative_point(
    point1: Point, point2: Point, dx: float, dy: float, dz: float
) -> None:
    assert point1.create_relative_point(dx, dy, dz) == point2


def test_create_relative_point_invalid(point1: Point) -> None:
    with pytest.raises(TypeError):
        point1.create_relative_point("dx", "dy", "dz")
