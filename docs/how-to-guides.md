# How-To Guides

## Creating panels for a vertical cylinder

```py linenums="1" title="cylinder.py"
import math
from pathlib import Path

from pymesh import Point, Line, Arc3P, ArcPVA, PlaneSurface, RuledSurface, SweptSurface
from pymesh import MeshGenerator, ExponentialDistribution
from pymesh import MeshViewer, GDFWriter

DIAMETER = 2.0
RATIO = 0.4
DEPTH = 1

# Create one quarter of the circle plate inner part
point00 = Point(0, 0, -DEPTH)
point10 = Point(RATIO * DIAMETER / 2, 0, -DEPTH)
point01 = Point(0, RATIO * DIAMETER / 2, -DEPTH)
PlaneSurface(point00, point10, point01).flip_normal()

# Create one quarter of the circle plate outer part
point11 = Point(RATIO * DIAMETER / 2, RATIO * DIAMETER / 2, -DEPTH)
point11c = Point(DIAMETER / 2 / math.sqrt(2), DIAMETER / 2 / math.sqrt(2), -DEPTH)
point10c = Point(DIAMETER / 2, 0, -DEPTH)
point01c = Point(0, DIAMETER / 2, -DEPTH)
line10 = Line(point10, point11)
arc10 = Arc3P(point00, point10c, point11c)
RuledSurface(line10, arc10).copy().mirror(a=-1, b=-1, c=0).flip_normal()

# Create a full circular plate by copying and rotating existing surfaces
for surface in RuledSurface.get_all_surfaces():
    for angle in (90, 180, 270):
        surface.copy().rotate(angle * math.pi / 180, a=0, b=0, c=1)

# Add surfaces to the mesh generator and set mesh settings
mesh = MeshGenerator()
for surface in RuledSurface.get_all_surfaces():
    mesh.add_surface(surface, density_u=0.2, density_w=0.2)

# Create cylinder surface
circle = ArcPVA(Point(DIAMETER / 2, 0, -DEPTH), 2 * math.pi, a=0, b=0, c=1)
line = Line(Point(0, 0, -DEPTH), Point(0, 0, 0))
surface_cylinder = SweptSurface(circle, line)

# Add cylinder surface to the mesh generator and set mesh settings
mesh.add_surface(
    surface_cylinder,
    density_u=0.2,  # float indicating panel length
    density_w=4,  # int specifying numper of panels
    distribution_w=ExponentialDistribution(flip_direction=True),
)

viewer = MeshViewer(mesh)
viewer.show()

writer = GDFWriter(mesh)
writer.write(filename=Path("output", "cylinder.gdf"))
```
