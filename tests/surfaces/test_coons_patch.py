"""Module for testing the Point class functionality"""

import numpy as np
import pytest

from pymesh import Point, Line, CoonsPatch
from pymesh.exceptions import CurveIntersectionError
from pymesh.geo.surfaces.surface import Surface


@pytest.fixture
def valid_points() -> tuple[Point]:
    p00 = Point(0, 0, 0)
    p11 = Point(1, 1, 0)
    p01 = Point(0, 1, 0)
    p10 = Point(1, 0, 0)
    return p00, p01, p10, p11


@pytest.fixture
def valid_lines(valid_points) -> tuple[Line]:
    p00, p01, p10, p11 = valid_points
    line_u0 = Line(p00, p10)
    line_u1 = Line(p11, p01)
    line_0w = Line(p01, p00)
    line_1w = Line(p11, p10)
    return line_u0, line_u1, line_0w, line_1w


@pytest.fixture
def lines_not_connected() -> tuple[Line]:
    p00 = Point(0, 0, 0)
    p11 = Point(1, 1, 0)
    p01 = Point(0, 1, 0)
    p10 = Point(1, 0, 0)
    p10_invalid = Point(2, 0, 0)
    line_u0 = Line(p00, p10)
    line_u1 = Line(p11, p01)
    line_0w = Line(p01, p00)
    line_1w_invalid = Line(p11, p10_invalid)
    return line_u0, line_u1, line_0w, line_1w_invalid


def test_init(valid_lines) -> None:
    CoonsPatch(valid_lines)


def test_init_invalid() -> None:
    with pytest.raises(TypeError):
        CoonsPatch("line_collection")


def test_init_lines_not_connected(lines_not_connected):
    with pytest.raises(CurveIntersectionError):
        CoonsPatch(lines_not_connected)


def test_curves(valid_lines) -> None:
    line_u0, line_u1, line_0w, line_1w = valid_lines
    curves = CoonsPatch((line_u0, line_0w, line_u1, line_1w)).curves
    assert curves == valid_lines


def test_get_all_surfaces(valid_lines) -> None:
    Surface._all_surfaces = []
    CoonsPatch(valid_lines)
    CoonsPatch(valid_lines)
    CoonsPatch(valid_lines)
    surfaces = CoonsPatch.get_all_surfaces()
    assert len(surfaces) == 3


def test_get_max_lengths(valid_lines) -> None:
    lengths = CoonsPatch(valid_lines).get_max_lengths()
    for length in lengths:
        assert length == 1.0


def test_path(valid_lines, assert_surface_rounded_path_xyz) -> None:
    surface = CoonsPatch(valid_lines)
    assert np.all(surface.path(0, 0, False, False) == np.array([0, 0, 0]))
    assert np.all(surface.path(1, 1, True, True) == np.array([0, 0, 0]))
    assert np.all(surface.path(0, 1, False, True) == np.array([0, 0, 0]))
    assert np.all(surface.path(1, 0, True, False) == np.array([0, 0, 0]))

    assert np.all(surface.path(1, 1, False, False) == np.array([1, 1, 0]))
    assert np.all(surface.path(0, 0, True, True) == np.array([1, 1, 0]))
    assert np.all(surface.path(1, 0, False, True) == np.array([1, 1, 0]))
    assert np.all(surface.path(0, 1, True, False) == np.array([1, 1, 0]))

    decimals = 4
    assert_surface_rounded_path_xyz(
        surface, 0.2, 0.2, False, False, np.array([0.2, 0.2, 0]), decimals
    )
    assert_surface_rounded_path_xyz(
        surface, 0.2, 0.2, True, True, np.array([0.8, 0.8, 0]), decimals
    )
