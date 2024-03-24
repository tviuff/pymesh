"""Module for testing the Point class functionality"""

import math

import numpy as np
import pytest

from pygdf import Point, Line


def test_init(point1: Point, point2: Point) -> None:
    Line(point1, point2)


def test_init_invalid() -> None:
    with pytest.raises(TypeError):
        Line("point1", "point2")


def test_eq(line1) -> None:
    assert line1 == line1


def test_point_end(point1: Point, point2: Point) -> None:
    point_end = Line(point1, point2).point_end
    assert isinstance(point_end, Point)
    assert point_end == point2


def test_point_start(point1: Point, point2: Point) -> None:
    point_start = Line(point1, point2).point_start
    assert isinstance(point_start, Point)
    assert point_start == point1


def test_length(point1: Point, point2: Point, dx, dy, dz) -> None:
    length = Line(point1, point2).length
    assert isinstance(length, float)
    assert length == math.sqrt(dx**2 + dy**2 + dz**2)


def test_get_path_fn(point1: Point, point2: Point) -> None:
    path_fn = Line(point1, point2).get_path_fn()
    assert np.all(path_fn(0) == point1.xyz)
    assert np.all(path_fn(1) == point2.xyz)
    assert np.all(path_fn(0, flip_direction=True) == point2.xyz)
    assert np.all(path_fn(1, flip_direction=True) == point1.xyz)
    assert np.all(path_fn(0.2) == point1.xyz + 0.2 * (point2.xyz - point1.xyz))
    assert np.all(
        path_fn(0.2, flip_direction=True)
        == point1.xyz + (1.0 - 0.2) * (point2.xyz - point1.xyz)
    )
