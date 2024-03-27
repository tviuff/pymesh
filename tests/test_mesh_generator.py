"""Module for testing the MeshGenerator class functionality"""

from collections.abc import Callable

import pytest

from pymesh import PlaneSurface, ExponentialDistribution, CosineDistribution
from pymesh.mesh.mesh_generator import MeshGenerator


@pytest.fixture
def mesher(p00, p01, p10) -> MeshGenerator:
    surface = PlaneSurface(p00, p01, p10)
    return MeshGenerator(surface.get_path(), surface.get_max_lengths())


def test_init(mesher) -> None:
    assert len(mesher.panel_densities) == 2
    assert len(mesher.mesh_distributions) == 2
    assert len(mesher.lengths) == 2
    assert isinstance(mesher.surface_fn, Callable)


def test_set_u_parameters(mesher) -> None:
    INDEX = 0
    mesher.set_u_parameters(panel_density=3, distribution=CosineDistribution())
    assert mesher.panel_densities[INDEX] == 3
    assert isinstance(mesher.mesh_distributions[INDEX], CosineDistribution)


def test_set_w_parameters(mesher) -> None:
    INDEX = 1
    mesher.set_w_parameters(panel_density=0.2, distribution=ExponentialDistribution())
    assert mesher.panel_densities[INDEX] == 0.2
    assert isinstance(mesher.mesh_distributions[INDEX], ExponentialDistribution)


def test_lengths(mesher) -> None:
    assert mesher.lengths == (1, 1)


def test_get_num_points(mesher) -> None:
    mesher.set_u_parameters(panel_density=3)
    mesher.set_w_parameters(panel_density=0.2)
    num_points = mesher._get_num_points()
    assert len(num_points) == 2
    assert num_points[0] == 4
    assert num_points[1] == 6


@pytest.mark.skip(reason="dummy test, not written")
def test_generate_mesh_points(mesher) -> None:
    points = mesher.generate_mesh_points()
