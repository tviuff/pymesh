"""Module initializer (constructor)
"""

# ! import order matters - Surface must be first ! #

from gdf.surfaces.surface import Surface
from gdf.surfaces.coons_patch import CoonsPatch
from gdf.surfaces.swept_surface import SweptSurface
from gdf.surfaces.plane_surface import PlaneSurface
from gdf.surfaces.bilinear_surface import BilinearSurface
from gdf.surfaces.ruled_surface import RuledSurface
