"""Rectangular surface example"""

import sys, os
sys.path.append(os.path.abspath(os.path.join('..', 'gdf')))

import math
from gdf import Point, Vector3D, ArcVA, GDFViewer

curve1 = ArcVA(
    vector_start = Vector3D(Point(0.5, 0, 0), Point(1, 0, 0)),
    vector_rot = Vector3D(Point(0, 0, 0), Point(0, 1, 1)),
    angle = 2*math.pi
    )
xyz = curve1.get_path_xyz(num_points=20)

viewer = GDFViewer()
viewer.add_curve_points(xyz)
viewer.show()
