"""Module for testing the Point class functionality"""

import math
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
        RuledSurface("", "")


@pytest.mark.skip(reason="Test not implemented")
def test_repr() -> None:
    pass


def test_curve_1(valid_lines) -> None:
    line1, line2 = valid_lines
    curve1 = RuledSurface(line1, line2).curve1
    assert np.all(curve1 == line1)


def test_curve_2(valid_lines) -> None:
    line1, line2 = valid_lines
    curve2 = RuledSurface(line1, line2).curve2
    assert np.all(curve2 == line2)


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


@pytest.mark.skip(reason="Test not implemented")
def test_path(p00, p01, p10, p11, test_surface_path) -> None:
    line1 = Line(p00, p01)
    line2 = Line(p10, p11)
    surface = RuledSurface(line1, line2)
    test_surface_path(surface, p00, p01, p10, p11)


def test_rotate(assert_rotate) -> None:
    angle = 90 * math.pi / 180
    line1 = Line(Point(0, 0, 0), Point(0, 1, 0))
    line2 = Line(Point(1, 0, 0), Point(1, 1, 0))
    surface = RuledSurface(line1, line2)
    line1_rotated = Line(Point(0, 0, 0), Point(-1, 0, 0))
    line2_rotated = Line(Point(0, 1, 0), Point(-1, 1, 0))
    surface_rotated = RuledSurface(line1_rotated, line2_rotated)
    assert_rotate(surface, surface_rotated, a=0, b=0, c=1, angle=angle)


def test_mirror(p00, p01, p10, p11) -> None:
    line1 = Line(p00, p01)
    line2 = Line(p10, p11)
    surface = RuledSurface(line1, line2)
    line1_mirror = Line(Point(0, 0, 0), Point(0, 1, 0))
    line2_mirror = Line(Point(-1, 0, 0), Point(-1, 1, 0))
    surface_mirror = RuledSurface(line1_mirror, line2_mirror)
    assert surface.mirror(1, 0, 0) == surface_mirror
