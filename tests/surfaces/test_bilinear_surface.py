"""Module for testing the BilinearSurface class functionality"""

import numpy as np
import pytest

from pymesh import BilinearSurface
from pymesh.geo.surfaces.surface import Surface


@pytest.fixture
def surface1(p00, p01, p10, p11) -> None:
    return BilinearSurface(p00, p10, p11, p01)


@pytest.mark.skip(reason="not implemented correct")
def test_init_invalid() -> None:
    with pytest.raises(TypeError):
        BilinearSurface("", "", "", "")


def test_bottom_left(surface1, p00) -> None:
    assert np.all(surface1.bottom_left == p00.xyz)


def test_bottom_right(surface1, p10) -> None:
    assert np.all(surface1.bottom_right == p10.xyz)


def test_top_right(surface1, p11) -> None:
    assert np.all(surface1.top_right == p11.xyz)


def test_top_left(surface1, p01) -> None:
    assert np.all(surface1.top_left == p01.xyz)


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


@pytest.mark.skip(reason="not found a way to test it yet")
def test_path(p00, p01, p10, p11, test_surface_path) -> None:
    surface = BilinearSurface(p00, p10, p11, p01)
    test_surface_path(surface, p00, p01, p10, p11)
