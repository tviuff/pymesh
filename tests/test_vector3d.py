"""Module for testing the Point class functionality"""

import numpy as np
import pytest

from pymesh import Vector3D


@pytest.fixture
def vector1(point1, point2) -> None:
    return Vector3D(point1, point2)


@pytest.fixture
def vector2(point1, point2, dx, dy, dz) -> None:
    point1.move(dx, dy, dz)
    point2.move(dx, dy, dz)
    return Vector3D(point1, point2)


@pytest.mark.skip(reason="not implemeted correct")
def test_init_invalid() -> None:
    with pytest.raises(TypeError):
        Vector3D("", "")


def test_eq(vector1) -> None:
    assert vector1 == vector1


def test_ne(vector1, vector2) -> None:
    assert vector1 != vector2


def test_repr(vector1, point1, point2) -> None:
    dx = point2.x - point1.x
    dy = point2.y - point1.y
    dz = point2.z - point1.z
    assert f"{vector1!r}" == f"Vector3D(dx={dx:.2f}, dy={dy:.2f}, dz={dz:.2f})"


def test_start(vector1, point1) -> None:
    assert isinstance(vector1.start, np.ndarray)
    assert np.all(vector1.start == point1.xyz)


def test_end(vector1, point2) -> None:
    assert isinstance(vector1.end, np.ndarray)
    assert np.all(vector1.end == point2.xyz)


def test_length(point1, point2) -> None:
    vector = Vector3D(point1, point2)
    length = np.sqrt(np.sum((point1.xyz - point2.xyz) ** 2))
    assert np.all(vector.length == length)


def test_unit_vector(point1, point2) -> None:
    vector = Vector3D(point1, point2)
    unit_vector = (vector.end - vector.start) / np.sqrt(
        np.sum((point1.xyz - point2.xyz) ** 2)
    )
    assert np.all(vector.unit_vector == unit_vector)


def test_copy(assert_copy, vector1) -> None:
    assert_copy(vector1)


def test_move(assert_move, vector1, vector2, dx, dy, dz) -> None:
    assert_move(vector1, vector2, dx, dy, dz)
