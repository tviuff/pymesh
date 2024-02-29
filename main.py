"""Main module for trying out code ideas
"""

from src import Point, Line

point1 = Point(0.0, 0.0, 0.0)
point2 = Point(1.0, 0.0, 0.0)
point3 = Point(1.0, 1.0, 0.0)
point4 = Point(0.0, 1.0, 0.0)

for point in [point1, point2, point3, point4]:
    print(point)

line1 = Line(point1, point2)
line2 = Line(point2, point3)
line3 = Line(point3, point4)
line4 = Line(point4, point1)

for line in [line1, line2, line3, line4]:
    print(line)
