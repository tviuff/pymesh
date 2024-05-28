"""Module for testing the UserDefinedCurve class functionality"""

from collections.abc import Callable
import math

import numpy as np
import pytest

from pymesh import Point, UserDefinedCurve
from pymesh.typing import NDArray3


TOLERANCE = 0.0001


@pytest.fixture
def user_path_fn():
    return lambda u: np.array([u, u, 0])


@pytest.fixture
def curve1():
    return UserDefinedCurve(lambda u: np.array([u, 0, 0]))


@pytest.fixture
def curve2():
    return UserDefinedCurve(lambda u: np.array([0, u, 0]))


def test_init(user_path_fn) -> None:
    UserDefinedCurve(user_path_fn)


def test_init_invalid() -> None:
    with pytest.raises(TypeError):
        UserDefinedCurve("path_fn")


@pytest.mark.skip("Not yet implemented")
def test_ne(curve1: UserDefinedCurve, curve2: UserDefinedCurve) -> None:
    assert curve1 != curve2


def test_repr(curve1: UserDefinedCurve) -> None:
    assert f"{curve1!r}" == "UserDefinedCurve(path=UserDefined)"


def test_start(user_path_fn: Callable[[float], NDArray3[np.float64]]) -> None:
    start = UserDefinedCurve(user_path_fn).start
    assert isinstance(start, Point)
    assert start == Point(0, 0, 0)


def test_end(user_path_fn: Callable[[float], NDArray3[np.float64]]) -> None:
    end = UserDefinedCurve(user_path_fn).end
    assert isinstance(end, Point)
    assert end == Point(1, 1, 0)


def test_length(user_path_fn) -> None:
    length = UserDefinedCurve(user_path_fn).length
    assert isinstance(length, float)
    assert np.isclose(length, math.sqrt(2), atol=TOLERANCE)


def test_get_path(user_path_fn) -> None:
    path = UserDefinedCurve(user_path_fn).get_path()
    assert np.isclose(path(0), user_path_fn(0)).all()
    assert np.isclose(path(0.5), user_path_fn(0.5)).all()
    assert np.isclose(path(0.5, flip=True), user_path_fn(0.5)).all()
    assert np.isclose(path(1), user_path_fn(1)).all()


@pytest.mark.skip("Not yet implemented")
def test_copy(assert_copy, curve1) -> None:
    assert_copy(curve1)


@pytest.mark.skip("Not yet implemented")
def test_move(assert_move, line1, line1_moved, dx, dy, dz) -> None:
    assert_move(line1, line1_moved, dx, dy, dz)


@pytest.mark.skip("Not yet implemented")
def test_rotate(assert_rotate, line1, line1_rotated, angle) -> None:
    assert_rotate(line1, line1_rotated, a=0, b=0, c=1, angle=angle)


@pytest.mark.skip("Not yet implemented")
def test_mirror() -> None:
    assert Line(Point(0, 0, 0), Point(0, 1, 0)).mirror(1, 0, 0) == Line(
        Point(0, 0, 0), Point(0, 1, 0)
    )
