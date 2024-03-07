"""Module including linee class
"""

from .curve import Curve
from ..point import Point
from ..mesh import DistributionMethod

class Arc3(Curve):
    """Circular arc generated from 3 points in space
    From https://en.wikipedia.org/wiki/Rodrigues%27_rotation_formula
    """
    __tolerance = 0.0001
    def __init__(self, point_start:Point, point_end, point_centre:Point):
        raise NotImplementedError("Arc3 not yet implemented.")
        if not (
            isinstance(point_start, Point)
            and isinstance(point_end, Point)
            and isinstance(point_centre, Point)
        ):
            raise TypeError()
        if (
            (point_start == point_end)
            or (point_start == point_centre)
            or (point_end == point_centre)
        ):
            raise ValueError()
        self.point_centre, self.point_start, self.point_end = point_centre, point_start, point_end
        self.__vector0 = point_start.xyz - point_centre.xyz
        self.__vector1 = point_end.xyz - point_centre.xyz
        self.__radius0 = np.sqrt(np.sum(self.__vector0**2))
        self.__radius1 = np.sqrt(np.sum(self.__vector1**2))
        self.__vector0_unit_vector = self.__vector0/self.__radius0
        self.__vector1_unit_vector = self.__vector1/self.__radius1
        assert (abs(self.__radius1 - self.__radius0) <= self.__tolerance), f'Radius not consistent. |point_start-point_centre| not equal to |point_end-point_centre|!'
        self.radius = self.__radius0
        self.__cross = np.cross(self.__vector0, self.__vector1)
        self.__plane_unit_normal = self.__cross / np.sqrt(np.sum(self.__cross**2))
        if ((self.__cross == 0).all() and (self.__vector0_unit_vector == -self.__vector1_unit_vector).all()):
            self.angle = math.pi
        elif ((self.__cross == 0).all() and (self.__vector0_unit_vector == self.__vector1_unit_vector).all()):
            self.angle = 0.
        else:
            self.angle = np.arccos(np.dot(self.__vector0, self.__vector1) / ( self.__radius0 * self.__radius1 ))

    def __eq__(self, other):
        return self.point_centre == other.point_centre \
            and self.point_start == other.point_start \
                and self.point_end == other.point_end

    def __repr__(self):
        return f'{self.__class__.__name__}({self.point_centre}, {self.point_start}, {self.point_end})'

    def get_path_fn(num_points:int, dist_method:DistributionMethod):
        assert (num_points > 1), f'N {num_points} is not larger than 1!'

    def get_points(self, N:int=10, method='linear'):
        assert (N > 1), f'N {N} is not larger than 1!'
        assert (method in ['linear', 'cosine', 'cos01', 'cos10']), f'method {method} not recognized!'
        plane_unit_normal, angle = self.__plane_unit_normal, self.angle
        xyz = np.zeros((N, 3))
        for i, u in enumerate(np.linspace(0, 1, N, endpoint=True)):
            v, k, a = self.__vector0, plane_unit_normal, angle
            uu = math.cos(math.pi*(1-u))/2+.5 if method == 'cosine' else math.cos(math.pi*u/2) if 'cos01' else 1-math.cos(math.pi*u/2) if 'cos10' else u
            xyz[i,:] = self.point_centre.xyz + v*math.cos(a*uu) + np.cross(k, v)*math.sin(a*uu) + k*np.cross(k, v)*(1-math.cos(a*uu))
        return xyz
