"""Rectangular surface example"""

import sys, os
sys.path.append(os.path.abspath(os.path.join('..', 'gdfgen')))

import math
from gdfgen import Point, Vector3D, ArcVA
from examples import plotting as plt

curve1 = ArcVA(
    vector_start = Vector3D(Point(0.5, 0, 0), Point(1, 0, 0)),
    vector_rot = Vector3D(Point(0, 0, 0), Point(0, 1, 1)),
    angle = 2*math.pi
    )
xyz = curve1.get_path_xyz(num_points=20)

plt.plot_curve_points(xyz, 270, 90, (-1, 1), (-1, 1), (-1, 1))
