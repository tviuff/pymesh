"""Module for testing the Point class functionality"""

import numpy as np
import pytest

from pymesh import Point, PlaneSurface
from pymesh.geo.surfaces.surface import Surface


@pytest.fixture
def point0(p00) -> Point:
    return p00


@pytest.fixture
def point1(p01) -> Point:
    return p01


@pytest.fixture
def point2(p10) -> Point:
    return p10


@pytest.fixture
def invalid_points() -> tuple[Point]:
    point0 = Point(0, 0, 0)
    point1 = Point(1, 0, 0)
    return point0, point1, point0


@pytest.fixture
def surface1(point0, point1, point2) -> None:
    return PlaneSurface(point0, point1, point2)


def test_init_invalid() -> None:
    with pytest.raises(TypeError):
        PlaneSurface("random")  # pylint: disable=no-value-for-parameter


def test_point0(point0, point1, point2) -> None:
    point0 = PlaneSurface(point0, point1, point2).point0
    assert np.all(point0 == point0)


def test_point1(point0, point1, point2) -> None:
    point1 = PlaneSurface(point0, point1, point2).point1
    assert np.all(point1 == point1)


def test_point2(point0, point1, point2) -> None:
    point2 = PlaneSurface(point0, point1, point2).point2
    assert np.all(point2 == point2)


def test_get_all_surfaces(point0, point1, point2) -> None:
    Surface._all_surfaces = []
    PlaneSurface(point0, point1, point2)
    PlaneSurface(point0, point1, point2)
    PlaneSurface(point0, point1, point2)
    surfaces = PlaneSurface.get_all_surfaces()
    assert len(surfaces) == 3


def test_get_max_lengths(surface1) -> None:
    lengths = surface1.get_max_lengths()
    for length in lengths:
        assert length == 1.0


def test_path(point0, point1, point2, test_surface_path) -> None:
    p00, p10, p01, p11 = point0, point1, point2, Point(1, 1, 0)
    surface = PlaneSurface(point0, point1, point2)
    test_surface_path(surface, p00, p01, p10, p11)


@pytest.mark.skip(reason="Not yet implemented")
def test_rotate(point0, point1, point2, axis, angle) -> None:
    surface = PlaneSurface(point0, point1, point2)
    surface_copy = surface.copy()
    surface_copy.rotate(axis, angle)
