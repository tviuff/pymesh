"""Circle panel example"""

import sys, os

sys.path.append(os.path.abspath(os.path.join("..", "pygdf")))

import math
from pymesh import Point, Line, Arc3P, ArcPVA, PlaneSurface, RuledSurface, SweptSurface
from pymesh import MeshGenerator, MeshViewer

DIAMETER = 2.0
RATIO = 0.4
DEPTH = 5

# Points forming an inner rectangle in the circle
point00 = Point(0, 0, -DEPTH)
point10 = Point(RATIO * DIAMETER / 2, 0, -DEPTH)
point01 = Point(0, RATIO * DIAMETER / 2, -DEPTH)
surface_rectangle = PlaneSurface(point00, point10, point01)
surface_rectangle.flip_normal()

# Points forming the outer surfaces of the circle
point11 = Point(RATIO * DIAMETER / 2, RATIO * DIAMETER / 2, -DEPTH)
point11c = Point(DIAMETER / 2 / math.sqrt(2), DIAMETER / 2 / math.sqrt(2), -DEPTH)
point10c = Point(DIAMETER / 2, 0, -DEPTH)
point01c = Point(0, DIAMETER / 2, -DEPTH)

# Outer surfaces of circle
line10 = Line(point10, point11)
arc10 = Arc3P(point00, point10c, point11c)
surface_circle10 = RuledSurface(line10, arc10)
line01 = Line(point01, point11)
arc01 = Arc3P(point00, point01c, point11c)
surface_circle01 = RuledSurface(line01, arc01)
surface_circle01.flip_normal()

for surface in tuple(RuledSurface.get_all_surfaces()):
    for angle in (90, 180, 270):
        surface.copy().rotate(angle * math.pi / 180, a=0, b=0, c=1)

mesh = MeshGenerator()
for surface in tuple(RuledSurface.get_all_surfaces()):
    mesh.add_surface(surface, density_u=0.2, density_w=0.2)

circle = ArcPVA(Point(DIAMETER / 2, 0, -DEPTH), 2 * math.pi, a=0, b=0, c=1)
circle_line = Line(Point(0, 0, -DEPTH), Point(0, 0, 0))
surface_cylinder = SweptSurface(circle, circle_line)

mesh.add_surface(surface_cylinder, density_u=0.2, density_w=1.0)

if __name__ == "__main__":
    viewer = MeshViewer(mesh, panel_normal_length=0.5)
    viewer.show()
