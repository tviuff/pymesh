"""Module for testing the SweptSurface class functionality"""

import pytest

from pymesh import Point, Line, SweptSurface
from pymesh.geo.surfaces.surface import Surface


@pytest.fixture
def curve(p00, p10) -> Line:
    return Line(p00, p10)


@pytest.fixture
def sweeper(p00, p01) -> Line:
    return Line(p00, p01)


@pytest.fixture
def lines_not_connected(p00, p10, p01) -> tuple[Line]:
    p0_invalid = Point(2, 0, 0)
    curve = Line(p00, p10)
    sweeper = Line(p0_invalid, p01)
    return curve, sweeper


def test_init_invalid() -> None:
    with pytest.raises(TypeError):
        SweptSurface("", "")


def test_init_lines_not_connected(lines_not_connected):
    curve, sweeper = lines_not_connected
    SweptSurface(curve, sweeper)


def test_get_all_surfaces(curve, sweeper) -> None:
    Surface._all_surfaces = []
    SweptSurface(curve, sweeper)
    SweptSurface(curve, sweeper)
    SweptSurface(curve, sweeper)
    surfaces = SweptSurface.get_all_surfaces()
    assert len(surfaces) == 3


def test_get_max_lengths(curve, sweeper) -> None:
    lengths = SweptSurface(curve, sweeper).get_max_lengths()
    for length in lengths:
        assert length == 1.0


def test_path(p00, p10, p01, p11, curve, sweeper, test_surface_path) -> None:
    surface = SweptSurface(curve, sweeper)
    test_surface_path(surface, p00, p01, p10, p11)
