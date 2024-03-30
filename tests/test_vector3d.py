"""Module for testing the Point class functionality"""

import math

import numpy as np
import pytest

from pymesh import Point, Vector3D


@pytest.fixture
def vector1(point1: Point, point2: Point) -> None:
    return Vector3D(point1, point2)


@pytest.fixture
def vector2(point1_moved: Point, point2_moved: Point) -> None:
    return Vector3D(point1_moved, point2_moved)


def test_init_invalid() -> None:
    with pytest.raises(TypeError):
        Vector3D("", "")


def test_ne(vector1: Vector3D, vector2: Vector3D) -> None:
    assert vector1 != vector2


def test_repr(vector1: Vector3D, point1: Point, point2: Point) -> None:
    assert f"{vector1!r}" == f"Vector3D(start={point1!r}, end={point2!r})"


def test_start(vector1: Vector3D, point1: Point) -> None:
    assert isinstance(vector1.start, Point)
    assert vector1.start == point1


def test_end(vector1: Vector3D, point2: Point) -> None:
    assert isinstance(vector1.end, Point)
    assert vector1.end == point2


def test_length(point1: Point, point2: Point) -> None:
    vector = Vector3D(point1, point2)
    length = np.sqrt(np.sum((point1.xyz - point2.xyz) ** 2))
    assert np.all(vector.length == length)


def test_unit_vector(point1: Point, point2: Point) -> None:
    vector = Vector3D(point1, point2)
    unit_vector = (vector.end.xyz - vector.start.xyz) / np.sqrt(
        np.sum((point1.xyz - point2.xyz) ** 2)
    )
    assert np.all(vector.unit_vector == unit_vector)


def test_copy(assert_copy, vector1: Vector3D) -> None:
    assert_copy(vector1)


def test_move(
    assert_move, vector1: Vector3D, vector2: Vector3D, dx: float, dy: float, dz: float
) -> None:
    assert_move(vector1, vector2, dx, dy, dz)


@pytest.mark.skip(reason="Test of deprocated implementation")
def test_rotate(p00, p10, p01) -> None:
    DECIMALS = 4
    axis = Vector3D(p00, Point(0, 0, 1))
    angle = 90 * math.pi / 180
    vector1 = Vector3D(p00, p10).rotate(axis, angle)
    vector2 = Vector3D(p00, p01)
    result = np.round(vector1.end.xyz, decimals=DECIMALS)
    expected = np.round(vector2.end.xyz, decimals=DECIMALS)
    assert np.all(result == expected)


def test_rotate(p00, p10, p01) -> None:
    DECIMALS = 4
    angle = 90 * math.pi / 180
    vector1 = Vector3D(p00, p10).rotate(angle, 0, 0, 1)
    vector2 = Vector3D(p00, p01)
    result = np.round(vector1.end.xyz, decimals=DECIMALS)
    expected = np.round(vector2.end.xyz, decimals=DECIMALS)
    print(result)
    print(expected)
    assert np.all(result == expected)


def test_mirror() -> None:
    assert Vector3D(Point(0, 0, 0), Point(0, 1, 0)).mirror(1, 0, 0) == Vector3D(
        Point(0, 0, 0), Point(0, 1, 0)
    )
    assert Vector3D(Point(0, 0, 0), Point(1, 0, 0)).mirror(1, 0, 0) == Vector3D(
        Point(0, 0, 0), Point(-1, 0, 0)
    )
    assert Vector3D(Point(0, 0, 0), Point(0, 1, 0)).mirror(0, 1, 0) == Vector3D(
        Point(0, 0, 0), Point(0, -1, 0)
    )
    assert Vector3D(Point(0, 0, 0), Point(1, 0, 0)).mirror(0, 1, 0) == Vector3D(
        Point(0, 0, 0), Point(1, 0, 0)
    )
    assert Vector3D(Point(0, 0, 0), Point(0, 0, 1)).mirror(0, 0, 1) == Vector3D(
        Point(0, 0, 0), Point(0, 0, -1)
    )

    assert Vector3D(Point(0, 0, 0), Point(2, 0, 0)).mirror(1, 0, 0, x0=1) == Vector3D(
        Point(2, 0, 0), Point(0, 0, 0)
    )
    assert Vector3D(Point(0, 0, 0), Point(0, 2, 0)).mirror(0, 1, 0, y0=1) == Vector3D(
        Point(0, 2, 0), Point(0, 0, 0)
    )
    assert Vector3D(Point(0, 0, 0), Point(0, 0, 3)).mirror(0, 0, 1, z0=2) == Vector3D(
        Point(0, 0, 4), Point(0, 0, 1)
    )
