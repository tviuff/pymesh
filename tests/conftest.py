# conftest.py

from collections.abc import Callable

import pytest
import numpy as np
from numpy import ndarray

from pymesh import Point, Line
from pymesh.geo.curves.curve import Curve
from pymesh.geo.surfaces.surface import Surface
from pymesh.typing import NDArray3


@pytest.fixture
def dx() -> int:
    return 0


@pytest.fixture
def dy() -> float:
    return -3.0


@pytest.fixture
def dz() -> float:
    return 4.0


@pytest.fixture
def point1() -> Point:
    return Point(0, 0, 0)


@pytest.fixture
def point2(
    dx: int | float, dy: int | float, dz: int | float
) -> Point:  # pylint: disable=redefined-outer-name
    return Point(dx, dy, dz)


@pytest.fixture
def line1(point1: Point, point2: Point) -> Line:  # pylint: disable=redefined-outer-name
    return Line(point1, point2)


@pytest.fixture
def line2(point1: Point, point2: Point) -> Line:  # pylint: disable=redefined-outer-name
    return Line(point2, point1)


@pytest.fixture
def assert_curve_rounded_path_xyz():
    def fn(
        curve: Curve, u: int | float, flip: bool, xyz: ndarray, decimals: int = 0
    ) -> None:
        result = np.round(curve.path(u, flip), decimals=decimals)
        expected = np.round(xyz, decimals=decimals)
        assert np.all(result == expected)

    return fn


@pytest.fixture
def assert_surface_rounded_path_xyz():
    def fn(
        surface: Surface,
        u: int | float,
        w: int | float,
        uflip: bool,
        wflip: bool,
        xyz: ndarray,
        decimals: int = 0,
    ) -> None:
        result = np.round(surface.path(u, w, uflip, wflip), decimals=decimals)
        expected = np.round(xyz, decimals=decimals)
        assert np.all(result == expected)

    return fn


@pytest.fixture
def assert_surface_corner_points() -> (
    Callable[[Surface, NDArray3, NDArray3, NDArray3, NDArray3], None]
):
    def fn(
        surface: Surface,
        p00: NDArray3,
        p01: NDArray3,
        p10: NDArray3,
        p11: NDArray3,
    ):
        assert np.all(surface.path(0, 0, False, False) == p00)
        assert np.all(surface.path(1, 1, True, True) == p00)
        assert np.all(surface.path(0, 1, False, True) == p00)
        assert np.all(surface.path(1, 0, True, False) == p00)

        assert np.all(surface.path(0, 1, False, False) == p01)
        assert np.all(surface.path(1, 0, True, True) == p01)
        assert np.all(surface.path(0, 0, False, True) == p01)
        assert np.all(surface.path(1, 1, True, False) == p01)

        assert np.all(surface.path(1, 0, False, False) == p10)
        assert np.all(surface.path(0, 1, True, True) == p10)
        assert np.all(surface.path(1, 1, False, True) == p10)
        assert np.all(surface.path(0, 0, True, False) == p10)

        assert np.all(surface.path(1, 1, False, False) == p11)
        assert np.all(surface.path(0, 0, True, True) == p11)
        assert np.all(surface.path(1, 0, False, True) == p11)
        assert np.all(surface.path(0, 1, True, False) == p11)

    return fn


# @pytest.fixture
# def assert_plane_surface_internal_points(
#     assert_surface_rounded_path_xyz,
# ) -> Callable[[Surface, NDArray3, NDArray3, NDArray3, NDArray3, int], None]:
#     def func(
#         surface: Surface,
#         p00: NDArray3,
#         p01: NDArray3,
#         p10: NDArray3,
#         p11: NDArray3,
#         decimals=4,
#     ):
#         def calculate_internal_point_xyz(u, w):
#             p1 = (1 - u) * w + u * w
#             p2 = (1 - w) * u + w * u
#             p3 = (
#                 (1 - u) * (1 - w) * p00
#                 + u * (1 - w) * p10
#                 + (1 - u) * w * p01
#                 + u * w * p11
#             )
#             return p1 + p2 - p3

#         for u in np.linspace(0, 1, num=10, endpoint=True):
#             for w in np.linspace(0, 1, num=10, endpoint=True):
#                 xyz = calculate_internal_point_xyz(u, w)
#                 assert_surface_rounded_path_xyz(
#                     surface, u, w, False, False, xyz, decimals
#                 )

#     return func
