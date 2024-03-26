"""Rectangular surface example"""

import sys, os

sys.path.append(os.path.abspath(os.path.join("..", "pygdf")))

from pymesh import (
    Point,
    PlaneSurface,
    ExponentialDistribution,
    MeshViewer,
)

point_0 = Point(0, 0, 0)
point_1 = Point(1, 0, 0)
point_2 = Point(0, 1, 0)

surface = PlaneSurface(point_0=point_0, point_1=point_1, point_2=point_2)
surface.flip_normal()
surface.mesher.set_u_parameters(panel_density=0.2)
surface.mesher.set_w_parameters(
    panel_density=0.2, distribution=ExponentialDistribution(flip_direction=True)
)

surface_selection = PlaneSurface.get_all_surfaces()

viewer = MeshViewer(panel_normal_length=0.5)
viewer.add_panels(surface_selection, include_normals=True)
viewer.show()
