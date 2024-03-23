"""Module containing most class descriptors
"""

class CartesianCoordinate:
    """Coordinate descriptor class"""

    def __set_name__(self, owner, name):
        self._name = name

    def __get__(self, instance, owner) -> float:
        return instance.__dict__[self._name]

    def __set__(self, instance, value):
        if not isinstance(value, (int, float)):
            raise TypeError(f"{self._name} must be of type 'int' or 'float'")
        instance.__dict__[self._name] = float(value)
