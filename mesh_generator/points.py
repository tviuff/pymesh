"""Module containing Point classes.
"""

import csv
import numpy as np

class Point:
    """Creates and handles point coordintes
    """
    def __init__(self, x: float, y: float, z: float):
        self.x, self.y, self.z, self.xyz = x, y, z, np.array([x, y, z])

    def __eq__(self, other):
        return (self.xyz == other.xyz).all()

    def __repr__(self):
        return f"{self.__class__.__name__}({self.x:.2f}, {self.y:.2f}, {self.z:.2f})"

    @classmethod
    def from_csv(cls, filename):
        """Reads points from a csv file
        """
        with open(filename, mode="r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            points = list(reader)

        for point in points:
            cls(
                x = float(point.get("x")),
                y = float(point.get("y")),
                z = float(point.get("z"))
                )
