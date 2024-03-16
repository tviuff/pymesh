"""Circle panel example"""

import sys, os
sys.path.append(os.path.abspath(os.path.join('..', 'gdfpy')))

import math

from gdfpy import Point, Vector3D, Line, ArcVA, SweptSurface, GDFViewer
from examples.circle import surface_selection

point_ctr = Point(0, 0, 0)
radius = math.sqrt(2**2 + 2**2)
line = Line(point_ctr, Point.set_relative_to(point_ctr, 0, 0, 1))
curve = ArcVA(
    vector_start = Vector3D(Point(0, 0, 0), Point(radius, 0, 0)),
    vector_rot = Vector3D(Point(0, 0, 0), Point(0, 0, 1)),
    angle = 2*math.pi
    )
surface_cylinder = SweptSurface(curve=curve, sweeper_curve=line)
surface_cylinder.num_points_curve = 30
surface_cylinder.num_points_sweeper_curve = 5

surface_selection = list(surface_selection)
surface_selection.append(surface_cylinder)

if __name__ == "__main__":
    viewer = GDFViewer(panel_normal_length=0.25)
    viewer.add_panels(
        surfaces = surface_selection,
        include_normals = True
        )
    viewer.show()
