"""Module for testing the Point class functionality"""

import pytest

from pygdf import Point, Line, Arc3P, ArcPVA, CoonsPatch
from pygdf.utils.exceptions import CurveIntersectionError

# ! Include flipped_curves in tests


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
    curves = CoonsPatch(valid_lines).curves
    assert curves == valid_lines


def test_panels(valid_lines) -> None:
    CoonsPatch(valid_lines).panels


def test__get_num_points(valid_lines) -> None:
    surface = CoonsPatch(valid_lines)
    surface.panel_density_u = 0.2
    surface.panel_density_w = 0.2
    assert len(surface.panels) == (1 / 0.2) * (1 / 0.2)
