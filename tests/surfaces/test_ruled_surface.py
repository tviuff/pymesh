"""Module for testing the Point class functionality"""

import numpy as np
import pytest

from pymesh import Point, Line, RuledSurface
from pymesh.geo.surfaces.surface import Surface


@pytest.fixture
def valid_lines(p00, p01, p10, p11) -> tuple[Line]:
    line1 = Line(p00, p01)
    line2 = Line(p10, p11)
    return line1, line2


@pytest.fixture
def surface1(valid_lines) -> None:
    line1, line2 = valid_lines
    return RuledSurface(line1, line2)


def test_init_invalid() -> None:
    with pytest.raises(TypeError):
        RuledSurface("random")  # pylint: disable=no-value-for-parameter


def test_curve_1(valid_lines) -> None:
    line1, line2 = valid_lines
    curve_1 = RuledSurface(line1, line2).curve_1
    assert np.all(curve_1 == line1)


def test_curve_2(valid_lines) -> None:
    line1, line2 = valid_lines
    curve_2 = RuledSurface(line1, line2).curve_2
    assert np.all(curve_2 == line2)


def test_get_all_surfaces(valid_lines) -> None:
    line1, line2 = valid_lines
    Surface._all_surfaces = []
    RuledSurface(line1, line2)
    RuledSurface(line1, line2)
    RuledSurface(line1, line2)
    surfaces = RuledSurface.get_all_surfaces()
    assert len(surfaces) == 3


def test_get_max_lengths(surface1) -> None:
    lengths = surface1.get_max_lengths()
    for length in lengths:
        assert length == 1.0


@pytest.mark.skip(reason="not found a way to test it yet")
def test_path(p00, p01, p10, p11, test_surface_path) -> None:
    line1 = Line(p00, p01)
    line2 = Line(p10, p11)
    surface = RuledSurface(line1, line2)
    test_surface_path(surface, p00, p01, p10, p11)
