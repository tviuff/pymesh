"""Circle panel example"""

import sys, os

sys.path.append(os.path.abspath(os.path.join("..", "pygdf")))

import math
from pymesh import Point, Line, Arc3P, PlaneSurface, RuledSurface, MeshViewer

# Points forming an inner rectangle in the circle
LENGTH = 0.8
point00 = Point(0, 0, 0)
point10 = Point(LENGTH / 2, 0, 0)
point01 = Point(0, LENGTH / 2, 0)
surface_rectangle = PlaneSurface(point00, point10, point01)
surface_rectangle.flip_normal()

# Points forming the outer surfaces of the circle
DIAMETER = 2.0
point11 = Point(LENGTH / 2, LENGTH / 2, 0)
point11c = Point(DIAMETER / 2 / math.sqrt(2), DIAMETER / 2 / math.sqrt(2), 0)
point10c = Point(DIAMETER / 2, 0, 0)
point01c = Point(0, DIAMETER / 2, 0)

# Outer surfaces of circle
line10 = Line(point10, point11)
arc10 = Arc3P(point00, point10c, point11c)
surface_circle10 = RuledSurface(line10, arc10)
line01 = Line(point01, point11)
arc01 = Arc3P(point00, point01c, point11c)
surface_circle01 = RuledSurface(line01, arc01)
surface_circle01.flip_normal()

surface_selection = RuledSurface.get_all_surfaces()

if __name__ == "__main__":
    viewer = MeshViewer(panel_normal_length=0.5)
    viewer.add_panels(surfaces=surface_selection, include_normals=True)
    viewer.show()
