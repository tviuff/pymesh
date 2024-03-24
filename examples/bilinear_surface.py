"""Bilinear surface example"""

import sys, os

sys.path.append(os.path.abspath(os.path.join("..", "pygdf")))

from pygdf import (
    Point,
    BilinearSurface,
    LinearDistribution,
    CosineDistribution,
    GDFViewer,
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
surface.panel_density_top_bottom = 10
surface.panel_density_left_right = 5
surface.distribution_top_bottom = CosineDistribution(flip_direction=False)
surface.distribution_left_right = LinearDistribution()

surface_selection = BilinearSurface.get_all_surfaces()

viewer = GDFViewer()
viewer.add_panels(surface_selection)
viewer.show()
