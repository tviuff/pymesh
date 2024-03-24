"""Circular curve example"""

import sys, os
sys.path.append(os.path.abspath(os.path.join('..', 'pygdf')))

import math
from pygdf import Point, Vector3D, ArcPVA, GDFViewer

curve1 = ArcPVA(
    point = Point(1, 0, 0),
    axis = Vector3D(Point(0, 0, 0), Point(0, -1, 1)),
    angle = 2*math.pi
    )
xyz = curve1.get_path_xyz(num_points=20)

viewer = GDFViewer()
viewer.add_curve_points(xyz)
viewer.show()
