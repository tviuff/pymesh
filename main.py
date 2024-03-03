"""Main module for trying out code ideas
"""

from mesh_generator import Point, Line

point1 = Point(0.0, 0.0, 0.0)
point2 = Point(1.0, 0.0, 0.0)
point3 = Point(1.0, 1.0, 0.0)
point4 = Point(0.0, 1.0, 0.0)

for point in [point1, point2, point3, point4]:
    print(point)
print()

line1 = Line(point1, point2)
line2 = Line(point2, point3)
line3 = Line(point3, point4)
line4 = Line(point4, point1)

for line in [line1, line2, line3, line4]:
    print(line)
print()

xyz = line1.get_points(n=5, method="cosine_end1")# needs better input text help

print(xyz)
print()

dist = Point.get_distance(point1, point2)
print(dist)
