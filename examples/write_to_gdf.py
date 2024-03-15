"""Write rectangular surface panels to gdf file"""

import sys, os
sys.path.append(os.path.abspath(os.path.join('..', 'gdfgen')))

from pathlib import Path
from gdfpy import Point, Line, CoonsPatch, GDFWriter

line1 = Line(Point(0, 0, 0), Point(1, 0, 0))
line2 = Line(Point(1, 0, 0), Point(1, 1, 0))
line3 = Line(Point(1, 1, 0), Point(0, 1, 0))
line4 = Line(Point(0, 1, 0), Point(0, 0, 0))
surface1 = CoonsPatch(line1, line3, line2, line4)

writer = GDFWriter()
writer.write(surface1, filename=Path("output", "rectangle.gdf"))
