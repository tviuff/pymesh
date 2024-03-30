"""Module for testing the Point class functionality"""

import math
import numpy as np
import pytest

from pymesh import Point, Line, CoonsPatch
from pymesh.exceptions import CurveIntersectionError
from pymesh.geo.surfaces.surface import Surface


@pytest.fixture
def valid_lines(p00, p01, p10, p11) -> tuple[Line]:
    line_u0 = Line(p00, p10)
    line_u1 = Line(p11, p01)
    line_0w = Line(p01, p00)
    line_1w = Line(p11, p10)
    return line_u0, line_u1, line_0w, line_1w


@pytest.fixture
def lines_not_connected(p00, p01, p10, p11) -> tuple[Line]:
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


@pytest.mark.skip(reason="Test not implemented")
def test_repr() -> None:
    pass


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


def test_path(p00, p01, p10, p11, valid_lines, test_surface_path) -> None:
    surface = CoonsPatch(valid_lines)
    test_surface_path(surface, p00, p01, p10, p11)


def test_rotate() -> None:
    DECIMALS = 4
    line_u0 = Line(Point(0, 0, 0), Point(1, 0, 0))
    line_u1 = Line(Point(1, 1, 0), Point(0, 1, 0))
    line_0w = Line(Point(0, 1, 0), Point(0, 0, 0))
    line_1w = Line(Point(1, 1, 0), Point(1, 0, 0))
    surface = CoonsPatch((line_u0, line_u1, line_0w, line_1w))
    angle = 90 * math.pi / 180
    rotated = surface.rotate(angle, a=0, b=0, c=1)
    rotated_corners = (
        np.round(rotated.path(0, 0), decimals=DECIMALS),
        np.round(rotated.path(1, 0), decimals=DECIMALS),
        np.round(rotated.path(1, 1), decimals=DECIMALS),
        np.round(rotated.path(0, 1), decimals=DECIMALS),
    )
    expected_corners = (
        np.array([0, 0, 0]),
        np.array([0, 1, 0]),
        np.array([-1, 1, 0]),
        np.array([-1, 0, 0]),
    )
    for rotated, expected in zip(rotated_corners, expected_corners):
        assert np.all(rotated == expected)


@pytest.mark.skip(reason="Test not implemented")
def test_mirror() -> None:
    pass
