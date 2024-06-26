"""Module for testing the Point class functionality"""

import math

import numpy as np
import pytest

from pymesh import Point, Line


def test_init(point1: Point, point2: Point) -> None:
    Line(point1, point2)


def test_init_invalid() -> None:
    with pytest.raises(TypeError):
        Line("point1", "point2")


def test_ne(line1: Line, line2: Line) -> None:
    assert line1 != line2


def test_repr(line1: Line) -> None:
    assert (
        f"{line1!r}"
        == "Line(start=Point(x=0.00, y=0.00, z=0.00), end=Point(x=0.00, y=-3.00, z=4.00))"
    )


def test_end(point1: Point, point2: Point) -> None:
    end = Line(point1, point2).end
    assert isinstance(end, Point)
    assert end == point2


def test_start(point1: Point, point2: Point) -> None:
    start = Line(point1, point2).start
    assert isinstance(start, Point)
    assert start == point1


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


def test_copy(assert_copy, line1) -> None:
    assert_copy(line1)


def test_move(assert_move, line1, line1_moved, dx, dy, dz) -> None:
    assert_move(line1, line1_moved, dx, dy, dz)


def test_rotate(assert_rotate, line1, line1_rotated, angle) -> None:
    assert_rotate(line1, line1_rotated, a=0, b=0, c=1, angle=angle)


def test_mirror() -> None:
    assert Line(Point(0, 0, 0), Point(0, 1, 0)).mirror(1, 0, 0) == Line(
        Point(0, 0, 0), Point(0, 1, 0)
    )
    assert Line(Point(0, 0, 0), Point(1, 0, 0)).mirror(1, 0, 0) == Line(
        Point(0, 0, 0), Point(-1, 0, 0)
    )
    assert Line(Point(0, 0, 0), Point(0, 1, 0)).mirror(0, 1, 0) == Line(
        Point(0, 0, 0), Point(0, -1, 0)
    )
    assert Line(Point(0, 0, 0), Point(1, 0, 0)).mirror(0, 1, 0) == Line(
        Point(0, 0, 0), Point(1, 0, 0)
    )
    assert Line(Point(0, 0, 0), Point(0, 0, 1)).mirror(0, 0, 1) == Line(
        Point(0, 0, 0), Point(0, 0, -1)
    )

    assert Line(Point(0, 0, 0), Point(2, 0, 0)).mirror(1, 0, 0, x0=1) == Line(
        Point(2, 0, 0), Point(0, 0, 0)
    )
    assert Line(Point(0, 0, 0), Point(0, 2, 0)).mirror(0, 1, 0, y0=1) == Line(
        Point(0, 2, 0), Point(0, 0, 0)
    )
    assert Line(Point(0, 0, 0), Point(0, 0, 3)).mirror(0, 0, 1, z0=2) == Line(
        Point(0, 0, 4), Point(0, 0, 1)
    )
