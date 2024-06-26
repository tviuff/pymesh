"""Module for testing the BilinearSurface class functionality"""

import math
import numpy as np
import pytest

from pymesh import Point, BilinearSurface
from pymesh.geo.surfaces.surface import Surface


@pytest.fixture
def surface1(p00, p01, p10, p11) -> None:
    return BilinearSurface(p00, p10, p11, p01)


def test_init_invalid() -> None:
    with pytest.raises(TypeError):
        BilinearSurface("", "", "", "")


@pytest.mark.skip(reason="Test not implemented")
def test_repr() -> None:
    pass


def test_bottom_left(surface1, p00) -> None:
    assert np.all(surface1.p00 == p00)


def test_bottom_right(surface1, p10) -> None:
    assert np.all(surface1.p10 == p10)


def test_top_right(surface1, p11) -> None:
    assert np.all(surface1.p11 == p11)


def test_top_left(surface1, p01) -> None:
    assert np.all(surface1.p01 == p01)


def test_get_all_surfaces(p00, p01, p10, p11) -> None:
    Surface._all_surfaces = []
    BilinearSurface(p00, p01, p11, p10)
    BilinearSurface(p00, p01, p11, p10)
    BilinearSurface(p00, p01, p11, p10)
    surfaces = BilinearSurface.get_all_surfaces()
    assert len(surfaces) == 3


def test_get_max_lengths(surface1) -> None:
    lengths = surface1.get_max_lengths()
    for length in lengths:
        assert length == 1.0


@pytest.mark.skip(reason="Test not implemented")
def test_path(p00, p01, p10, p11, test_surface_path) -> None:
    surface = BilinearSurface(p00, p10, p11, p01)
    test_surface_path(surface, p00, p01, p10, p11)


def test_rotate(assert_rotate) -> None:
    angle = 90 * math.pi / 180
    surface = BilinearSurface(
        Point(0, 0, 0), Point(1, 0, 0), Point(1, 1, 0), Point(0, 1, 0)
    )
    surface_rotated = BilinearSurface(
        Point(0, 0, 0), Point(0, 1, 0), Point(-1, 1, 0), Point(-1, 0, 0)
    )
    assert_rotate(surface, surface_rotated, a=0, b=0, c=1, angle=angle)


def test_mirror() -> None:
    surface = BilinearSurface(
        Point(0, 0, 0), Point(1, 0, 0), Point(1, 1, 0), Point(0, 1, 0)
    )
    surface_mirror = BilinearSurface(
        Point(0, 0, 0), Point(-1, 0, 0), Point(-1, 1, 0), Point(0, 1, 0)
    )
    assert surface.mirror(1, 0, 0) == surface_mirror
    surface = BilinearSurface(
        Point(0, 0, 0), Point(1, 0, 0), Point(1, 1, 0), Point(0, 1, 0)
    )
    surface_mirror = BilinearSurface(
        Point(0, 0, 0), Point(1, 0, 0), Point(1, -1, 0), Point(0, -1, 0)
    )
    assert surface.mirror(0, 1, 0) == surface_mirror
