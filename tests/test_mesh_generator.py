"""Module for testing the MeshGenerator class functionality"""

from collections.abc import Callable

import pytest

from pymesh import BilinearSurface, ExponentialDistribution, CosineDistribution
from pymesh.mesh.mesh_generator import MeshGenerator


@pytest.fixture
def mesher() -> MeshGenerator:
    return MeshGenerator()


@pytest.fixture
def surface(p00, p01, p11, p10) -> None:
    return BilinearSurface(p00, p01, p11, p10)


def test_init_invalid() -> None:
    with pytest.raises(TypeError):
        MeshGenerator("")


def test_add_surface(mesher, surface) -> None:
    mesher.add_surface(surface)


def test_get_num_points(mesher, surface) -> None:
    mesher.add_surface(surface)
    assert mesher.get_num_points(1, 0.2) == 6
    assert mesher.get_num_points(1, 1) == 2


def test__generate_mesh_points(mesher, surface) -> None:
    mesher.add_surface(surface)
    mesh = mesher.surfaces[0]
    mesh_points = mesher._generate_mesh_points(mesh)


def test__generate_panels(mesher, surface) -> None:
    mesher.add_surface(surface)
    mesh = mesher.surfaces[0]
    mesh_points = mesher._generate_mesh_points(mesh)
    mesh_points = mesher._generate_panels(mesh_points, flipped_normal=True)


def test_get_panels(mesher, surface) -> None:
    mesher.add_surface(surface)
    panels = mesher.get_panels()
