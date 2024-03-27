"""Module for testing the SweptSurface class functionality"""

import pytest

from pymesh import Point, Line, SweptSurface
from pymesh.geo.surfaces.surface import Surface


@pytest.fixture
def valid_points() -> tuple[Point]:
    p0 = Point(0, 0, 0)
    p1 = Point(1, 0, 0)
    p2 = Point(0, 1, 0)
    return p0, p1, p2


@pytest.fixture
def valid_lines(valid_points) -> tuple[Line]:
    p0, p1, p2 = valid_points
    curve = Line(p0, p1)
    sweeper = Line(p0, p2)
    return curve, sweeper


@pytest.fixture
def lines_not_connected(valid_points) -> tuple[Line]:
    p0, p1, p2 = valid_points
    p0_invalid = Point(2, 0, 0)
    curve = Line(p0, p1)
    sweeper = Line(p0_invalid, p2)
    return curve, sweeper


def test_init(valid_lines) -> None:
    curve, sweeper = valid_lines
    SweptSurface(curve, sweeper)


def test_init_invalid() -> None:
    with pytest.raises(TypeError):
        SweptSurface("line_collection")  # pylint: disable=no-value-for-parameter


def test_init_lines_not_connected(lines_not_connected):
    curve, sweeper = lines_not_connected
    SweptSurface(curve, sweeper)


def test_get_all_surfaces(valid_lines) -> None:
    Surface._all_surfaces = []
    curve, sweeper = valid_lines
    SweptSurface(curve, sweeper)
    SweptSurface(curve, sweeper)
    SweptSurface(curve, sweeper)
    surfaces = SweptSurface.get_all_surfaces()
    assert len(surfaces) == 3


def test_get_max_lengths(valid_lines) -> None:
    curve, sweeper = valid_lines
    lengths = SweptSurface(curve, sweeper).get_max_lengths()
    for length in lengths:
        assert length == 1.0


def test_path(valid_points, valid_lines, test_surface_path) -> None:
    p00, p10, p01 = valid_points
    p11 = Point(1, 1, 0)
    curve, sweeper = valid_lines
    surface = SweptSurface(curve, sweeper)
    test_surface_path(surface, p00, p01, p10, p11)
