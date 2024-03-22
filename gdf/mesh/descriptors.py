"""Module with curve distibution classes
"""

from gdf.mesh.distribution_methods import DistributionMethod

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

class PanelDensity:
    """Panel density descriptor class"""

    def __set_name__(self, owner, name):
        self._name = name

    def __get__(self, instance, owner) -> int|float:
        """get"""
        return instance.__dict__[self._name]

    def __set__(self, instance, value:int|float):
        """set"""
        if not isinstance(value, (int, float)):
            raise TypeError(f"{self._name} must be of type 'int' or 'float'")
        if value == 0:
            raise ValueError(f"{self._name} must be larger than zero")
        instance.__dict__[self._name] = value

class BoundaryDistribution:
    """Boundary dustribution descriptor class used for dist_u0 and others"""

    def __set_name__(self, owner, name):
        self._name = name

    def __get__(self, instance, owner) -> DistributionMethod:
        return instance.__dict__[self._name]

    def __set__(self, instance, value:DistributionMethod):
        if not isinstance(value, DistributionMethod):
            raise TypeError(f"{self._name} must be and instance of a subclass of 'DistributionMethod'")
        instance.__dict__[self._name] = value
