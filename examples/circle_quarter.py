"""Circle panel example"""

import sys, os

sys.path.append(os.path.abspath(os.path.join("..", "pygdf")))

import math
from pymesh import Point, Line, Arc3P, PlaneSurface, RuledSurface, MESHViewer

# Points forming an inner rectangle in the circle
square_size = 0.8
point00 = Point(0, 0, 0)
point10 = Point(square_size / 2, 0, 0)
point01 = Point(0, square_size / 2, 0)
surface_rectangle = PlaneSurface(point00, point10, point01)

# Points forming the outer surfaces of the circle
circle_diameter = 2.0
point11 = Point(square_size / 2, square_size / 2, 0)
point11c = Point(
    circle_diameter / 2 / math.sqrt(2), circle_diameter / 2 / math.sqrt(2), 0
)
point10c = Point(circle_diameter / 2, 0, 0)
point01c = Point(0, circle_diameter / 2, 0)

# Outer surfaces of circle
line10 = Line(point10, point11)
arc10 = Arc3P(point00, point10c, point11c)
surface_circle10 = RuledSurface(line10, arc10)
surface_circle10.flip_panel_normals()
line01 = Line(point01, point11)
arc01 = Arc3P(point00, point01c, point11c)
surface_circle01 = RuledSurface(line01, arc01)

surface_selection = RuledSurface.get_all_surfaces()

if __name__ == "__main__":
    viewer = MESHViewer(panel_normal_length=0.5)
    viewer.add_panels(surfaces=surface_selection, include_normals=True)
    viewer.show()
