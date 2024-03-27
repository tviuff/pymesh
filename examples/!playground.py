"""code playground"""

import sys, os

sys.path.append(os.path.abspath(os.path.join("..", "pygdf")))

from pymesh import Point, Line, Arc3P, SweptSurface, MeshViewer


line = Line(Point(0, 0, 0), Point(0, 0, 1))
curve = Arc3P(Point(0, 0, 0), Point(1, 0, 0), Point(1, 0.0001, 0))
curve.inverse_sector = True
surface = SweptSurface(curve, line)
surface.mesher.set_u_parameters(panel_density=30)
surface.flip_normal()

surface_selection = surface

viewer = MeshViewer(panel_normal_length=0.25)
viewer.add_panels(surface_selection, include_normals=True)
viewer.show()
