"""Rectangular surface example"""

import sys, os
sys.path.append(os.path.abspath(os.path.join('..', 'pygdf')))

from pygdf import Point, Arc3P, GDFViewer

curve1 = Arc3P(Point(0, 0, 0), Point(1, 0, 0), Point(1, 0.01, 0))
curve1.invert_arc = True
xyz = curve1.get_path_xyz(num_points=30)

viewer = GDFViewer()
viewer.add_curve_points(xyz)
viewer.show()
