"""Rectangular surface example"""

import sys, os
sys.path.append(os.path.abspath(os.path.join('..', 'gdfgen')))

from gdfgen import Point, Line, CoonsPatch
from examples import plotting as plt

point1 = Point(0, 0, 0)
point2 = Point.set_relative_to(point1, dx=1.0)
point3 = Point(1, 1, 0)
point4 = Point(0, 1, 0)

line1 = Line(point1, point2)
line2 = Line(point2, point3)
line3 = Line(point3, point4)
line4 = Line(point4, point1)

surface1 = CoonsPatch(line1, line3, line2, line4)
surface1.num_points_u = 10
surface1.num_points_w = 10

plt.plot_panels(surface1, 270, 90, (-1, 1), (-1, 1), (-1, 1))
