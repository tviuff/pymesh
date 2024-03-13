"""Module includes the ArcVA class
"""

import math
import numpy as np
from numpy import ndarray

from gdfgen import Point, Vector3D
from gdfgen.curves import Curve
from gdfgen.mesh import DistMethod
from gdfgen.constants import MeshConstants

class ArcVA(Curve):
    """Circular arc generated from a point, an angle (rad) and a vector axis of rotation
    For more iformation, see https://en.wikipedia.org/wiki/Rodrigues%27_rotation_formula.
    """

    def __init__(self, vector_start:Vector3D, vector_rot:Vector3D, angle:float):
        self.vector_start = vector_start
        self.vector_rot = vector_rot
        self.angle = angle
        self.point_start = vector_start.point_end

    @property
    def point_end(self) -> Point:
        v = self.vector_start.unit_vector * self.vector_start.length
        k = self.vector_rot.unit_vector * self.vector_rot.length
        a = self.angle
        xyz_end = self.vector_start.point_start.xyz \
                + v * math.cos(a) \
                + np.cross(k, v) * math.sin(a) \
                + k * np.dot(k, v) * (1 - math.cos(a))
        return Point(xyz_end[0], xyz_end[1], xyz_end[2])

    @property
    def vector_start(self) -> Vector3D:
        return self._vector_start

    @vector_start.setter
    def vector_start(self, value) -> None:
        if not isinstance(value, Vector3D):
            raise TypeError("vector_start must be of type 'Vector3D'")
        self._vector_start = value

    @property
    def vector_rot(self) -> Vector3D:
        return self._vector_rot

    @vector_rot.setter
    def vector_rot(self, value) -> None:
        if not isinstance(value, Vector3D):
            raise TypeError("vector_rot must of type 'Vector3D'")
        self._vector_rot = value

    @property
    def angle(self) -> float:
        return self._angle

    @angle.setter
    def angle(self, value) -> None:
        if not isinstance(value, float):
            raise TypeError("angle must of type 'float'")
        self._angle = value

    def __eq__(self, other):
        return self.vector_start == other.vector_start \
            and self.vector_rot == other.vector_rot \
                and self.angle == other.angle

    def __repr__(self):
        txt = f"{type(self).__name__}(vector_start={self.vector_start}, " \
                f"vector_rot={self.vector_rot}, angle={self.angle})"
        return txt

    def get_path_xyz(self,
            num_points:int = MeshConstants.DEFAULT_NUM_POINT.value,
            dist_method:DistMethod = MeshConstants.DEFAULT_DIST_METHOD.value,
            flip_dir:bool = False
        ) -> ndarray:
        path_xyz = np.zeros((num_points, 3))
        dist_fn = dist_method.get_fn(flip_dir)
        v = self.vector_start.unit_vector * self.vector_start.length
        k = self.vector_rot.unit_vector * self.vector_rot.length
        a = self.angle
        for i, u in enumerate(np.linspace(0, 1, num_points, endpoint=True)):
            path_xyz[i,:] = self.vector_start.point_start.xyz \
                    + v * math.cos(a * dist_fn(u)) \
                    + np.cross(k, v) * math.sin(a * dist_fn(u)) \
                    + k * np.dot(k, v) * (1 - math.cos(a * dist_fn(u)))
        return path_xyz
