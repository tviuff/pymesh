from collections.abc import Callable
import math

import numpy as np
import pytest

from pymesh import Point, UserDefinedCurve
from pymesh.typing import NDArray3


TOLERANCE = 0.0001


@pytest.fixture
def user_path_fn() -> Callable[[int | float], np.ndarray]:
    return lambda u: np.array([u, u, 0])


@pytest.fixture
def curve1() -> UserDefinedCurve:
    return UserDefinedCurve(lambda u: np.array([u, 0, 0]))


@pytest.fixture
def curve2() -> UserDefinedCurve:
    return UserDefinedCurve(lambda u: np.array([0, u, 0]))


def test_init(user_path_fn) -> None:
    UserDefinedCurve(user_path_fn)


def test_init_invalid() -> None:
    with pytest.raises(TypeError):
        UserDefinedCurve("path_fn")


def test_ne(curve1, curve2) -> None:
    assert curve1 != curve2


def test_repr(curve1) -> None:
    assert f"{curve1!r}" == "UserDefinedCurve(path=UserDefined)"


def test_start(user_path_fn) -> None:
    start = UserDefinedCurve(user_path_fn).start
    assert isinstance(start, Point)
    assert start == Point(0, 0, 0)


def test_end(user_path_fn) -> None:
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


def test_copy(assert_copy, curve1) -> None:
    assert_copy(curve1)


def test_move(assert_move, user_path_fn, dx, dy, dz) -> None:
    def moved_path(u):
        return user_path_fn(u) + np.array([dx, dy, dz])

    curve = UserDefinedCurve(user_path_fn)
    curve_moved = UserDefinedCurve(moved_path)

    assert_move(curve, curve_moved, dx, dy, dz)


def test_rotate(assert_rotate, curve1, curve2, angle) -> None:
    assert_rotate(curve1, curve2, 0, 0, 1, angle)


def test_mirror() -> None:
    curve = UserDefinedCurve(lambda u: np.array([u, u, 0]))
    curve_mirrored_in_xz_plane = UserDefinedCurve(lambda u: np.array([u, -u, 0]))
    assert curve.mirror(0, 1, 0) == curve_mirrored_in_xz_plane
