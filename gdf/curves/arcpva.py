"""Module includes the ArcVA class
"""

import math
import numpy as np
from numpy import ndarray

from gdf import Point, Vector3D
from gdf.curves import Curve
from gdf.mesh.distribution_methods import DistMethod
from gdf.constants import MeshConstants

class ArcPVA(Curve):
    """Circular arc generated from a point, an axis of rotation and an angle (rad).
    For more iformation, see https://en.wikipedia.org/wiki/Rodrigues%27_rotation_formula.
    """

    def __init__(self, point:Point, axis:Vector3D, angle:float):
        self.point_start = point
        self.axis = axis
        self.angle = angle

    @property
    def point_start(self) -> Point:
        return self._point_start

    @point_start.setter
    def point_start(self, value) -> None:
        if not isinstance(value, Point):
            raise TypeError("point_start must be of type 'Point'")
        self._point_start = value

    @property
    def point_end(self) -> Point:
        xyz = self.get_path_xyz(num_points=2)[-1, :]
        return Point(xyz[0], xyz[1], xyz[2])

    @property
    def vector_point(self) -> Vector3D:
        xyz0 = self.axis.point_start.xyz
        xyz1 = self.point_start.xyz
        point0 = Point(xyz0[0], xyz0[1], xyz0[2])
        point1 = Point(xyz1[0], xyz1[1], xyz1[2])
        return Vector3D(point0, point1)

    @property
    def axis(self) -> Vector3D:
        return self._axis

    @axis.setter
    def axis(self, value) -> None:
        if not isinstance(value, Vector3D):
            raise TypeError("axis must of type 'Vector3D'")
        self._axis = value

    @property
    def angle(self) -> float:
        return self._angle

    @angle.setter
    def angle(self, value) -> None:
        if not isinstance(value, float):
            raise TypeError("angle must of type 'float'")
        self._angle = value

    @property
    def radius(self) -> float:
        a = self.vector_point.point_end.xyz - self.vector_point.point_start.xyz
        b = self.axis.point_end.xyz - self.axis.point_start.xyz
        r = a - np.dot(a, b)/np.dot(b, b)*b
        return np.sqrt(np.sum(r**2))

    @property
    def length(self) -> float:
        return self.radius * self.angle

    def __eq__(self, other):
        return self.vector_point == other.vector_point \
            and self.axis == other.axis \
                and self.angle == other.angle

    def __repr__(self):
        txt = f"{type(self).__name__}(point={self.point_start}, " \
                f"axis={self.axis}, angle={self.angle})"
        return txt

    def get_path_xyz(self,
            num_points:int = None,
            dist_method:DistMethod = None,
            flip_dir:bool = False
        ) -> ndarray:
        if num_points is None:
            num_points = MeshConstants.DEFAULT_NUM_POINT.value
        if dist_method is None:
            dist_method = MeshConstants.DEFAULT_DIST_METHOD.value
        path_xyz = np.zeros((num_points, 3))
        dist_fn = dist_method.get_fn(flip_dir)
        xyz0 = self.vector_point.point_start.xyz
        v = self.vector_point.unit_vector * self.vector_point.length
        k = self.axis.unit_vector * self.axis.length
        a = self.angle
        for i, u in enumerate(np.linspace(0, 1, num_points, endpoint=True)):
            path_xyz[i,:] = xyz0 \
                    + v * math.cos(a * dist_fn(u)) \
                    + np.cross(k, v) * math.sin(a * dist_fn(u)) \
                    + k * np.dot(k, v) * (1 - math.cos(a * dist_fn(u)))
        return path_xyz
