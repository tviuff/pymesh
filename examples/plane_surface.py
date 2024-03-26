"""Rectangular surface example"""

import sys, os

sys.path.append(os.path.abspath(os.path.join("..", "pygdf")))

from pymesh import (
    Point,
    PlaneSurface,
    LinearDistribution,
    ExponentialDistribution,
    MeshViewer,
)

point_0 = Point(0, 0, 0)
point_1 = Point(1, 0, 0)
point_2 = Point(0, 1, 0)

surface = PlaneSurface(point_0=point_0, point_1=point_1, point_2=point_2)
surface.mesher.panel_densities = (0.2, 0.2)
surface.mesher.mesh_distributions = (
    LinearDistribution(),
    ExponentialDistribution(flip_direction=True),
)

surface_selection = PlaneSurface.get_all_surfaces()

viewer = MeshViewer()
viewer.add_panels(surface_selection, include_normals=True)
viewer.show()
