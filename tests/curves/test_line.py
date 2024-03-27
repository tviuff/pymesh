"""Module for testing the Point class functionality"""

import math

import numpy as np
import pytest

from pymesh import Point, Line


def test_init(point1: Point, point2: Point) -> None:
    Line(point1, point2)


def test_init_invalid() -> None:
    with pytest.raises(AttributeError):
        Line("point1", "point2")


def test_eq(line1, line2) -> None:
    assert line1 == line1
    assert line2 == line2


def test_ne(line1, line2) -> None:
    assert line1 != line2


def test_repr(line1) -> None:
    assert (
        f"{line1!r}"
        == "Line(start=Point(x=0.00, y=0.00, z=0.00), end=Point(x=0.00, y=-3.00, z=4.00))"
    )


def test_end(point1: Point, point2: Point) -> None:
    end = Line(point1, point2).end
    assert isinstance(end, np.ndarray)
    assert np.all(end == point2.xyz)


def test_start(point1: Point, point2: Point) -> None:
    start = Line(point1, point2).start
    assert isinstance(start, np.ndarray)
    assert np.all(start == point1.xyz)


def test_length(point1: Point, point2: Point, dx, dy, dz) -> None:
    length = Line(point1, point2).length
    assert isinstance(length, float)
    assert length == math.sqrt(dx**2 + dy**2 + dz**2)


def test_get_path(point1: Point, point2: Point) -> None:
    path = Line(point1, point2).get_path()
    assert np.all(path(0) == point1.xyz)
    assert np.all(path(1) == point2.xyz)
    assert np.all(path(0, flip=True) == point2.xyz)
    assert np.all(path(1, flip=True) == point1.xyz)
    assert np.all(path(0.2) == point1.xyz + 0.2 * (point2.xyz - point1.xyz))
    assert np.all(
        path(0.2, flip=True) == point1.xyz + (1.0 - 0.2) * (point2.xyz - point1.xyz)
    )
