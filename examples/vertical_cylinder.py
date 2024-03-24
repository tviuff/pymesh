"""Circle panel example"""

import sys, os
sys.path.append(os.path.abspath(os.path.join('..', 'pygdf')))

import math

from pygdf import Point, Vector3D, Line, ArcPVA, SweptSurface, GDFViewer
from examples.circle import surface_selection

point_ctr = Point(0, 0, 0)
radius = math.sqrt(2**2 + 2**2)
line = Line(point_ctr, point_ctr.create_relative_point(0, 0, 1))
curve = ArcPVA(
    point = Point(radius, 0, 0),
    axis = Vector3D(point_ctr, Point(0, 0, 1)),
    angle = 2*math.pi
    )
surface_cylinder = SweptSurface(curve=curve, sweeper_curve=line)
surface_cylinder.num_points_curve = 30
surface_cylinder.num_points_sweeper_curve = 5

surface_selection = list(surface_selection)
surface_selection.append(surface_cylinder)

if __name__ == "__main__":
    viewer = GDFViewer(panel_normal_length=0.5)
    viewer.add_panels(
        surfaces = surface_selection,
        include_normals = True
        )
    viewer.show()
