"""Module with curve distibution classes
"""

from gdf.mesh.distribution_methods import DistMethod

class MeshNumber:
    """Mesh number descriptor class used for num_points"""

    def __set_name__(self, owner, name):
        self._name = name

    def __get__(self, instance, owner) -> int:
        return instance.__dict__[self._name]

    def __set__(self, instance, value:int):
        if not isinstance(value, int):
            raise TypeError(f"{self._name} must be of type 'int'")
        instance.__dict__[self._name] = value

class BoundaryDistribution:
    """Boundary dustribution descriptor class used for dist_u0 and others"""

    def __set_name__(self, owner, name):
        self._name = name

    def __get__(self, instance, owner) -> DistMethod:
        return instance.__dict__[self._name]

    def __set__(self, instance, value:DistMethod):
        if not isinstance(value, DistMethod):
            raise TypeError(f"{self._name} must be and instance of a subclass of 'DistMethod'")
        instance.__dict__[self._name] = value
