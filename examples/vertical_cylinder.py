"""Circle panel example"""

import sys, os

sys.path.append(os.path.abspath(os.path.join("..", "pygdf")))

import math

from pymesh import Point, Line, ArcPVA, SweptSurface, MeshViewer
from examples.circle import surface_selection

point_ctr = Point(0, 0, 0)
radius = math.sqrt(2**2 + 2**2)
line = Line(point_ctr, point_ctr.create_relative_point(0, 0, 1))
curve = ArcPVA(Point(radius, 0, 0), 2 * math.pi, a=0, b=0, c=1)
surface_cylinder = SweptSurface(curve, line)
surface_cylinder.mesher.set_u_parameters(panel_density=30)
surface_cylinder.mesher.set_w_parameters(panel_density=5)

surface_selection = list(surface_selection)
surface_selection.append(surface_cylinder)

if __name__ == "__main__":
    viewer = MeshViewer(panel_normal_length=0.5)
    viewer.add_panels(surfaces=surface_selection, include_normals=True)
    viewer.show()
