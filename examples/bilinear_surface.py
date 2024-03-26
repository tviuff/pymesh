"""Bilinear surface example"""

import sys, os

sys.path.append(os.path.abspath(os.path.join("..", "pygdf")))

from pymesh import (
    Point,
    BilinearSurface,
    LinearDistribution,
    ExponentialDistribution,
    MeshViewer,
)

point00 = Point(0, 0, 0)
point10 = Point(1, 0, -1)
point11 = Point(1, 1, 0)
point01 = Point(0, 1, 0)

surface = BilinearSurface(
    point_bottom_left=point00,
    point_bottom_right=point10,
    point_top_right=point11,
    point_top_left=point01,
)

surface.mesher.panel_densities = (5, 10)
surface.mesher.mesh_distributions = (
    LinearDistribution(),
    ExponentialDistribution(flip_direction=False),
)

surface_selection = BilinearSurface.get_all_surfaces()

viewer = MeshViewer()
viewer.add_panels(surface_selection)
viewer.show()
