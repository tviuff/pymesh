"""Module with curve distibution classes
"""

from gdf import Point


class SurfaceCornerPoint:
    """Surface corner point descriptor class"""

    def __set_name__(self, owner, name):
        self._name = name

    def __get__(self, instance, owner) -> Point:
        return instance.__dict__[self._name]

    def __set__(self, instance, value):
        if not isinstance(value, Point):
            raise TypeError(f"{self._name} must be of type 'Point'")
        instance.__dict__[self._name] = value
