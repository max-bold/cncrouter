from collections.abc import MutableSequence
from typing import SupportsIndex, Self
import numpy as np


class Point:
    def __init__(self, x, y, z) -> None:
        self.x = x
        self.y = y
        self.z = z

    @property
    def asarray(self) -> np.ndarray:
        return np.array((self.x, self.y, self.x))

    def fromarray(a: SupportsIndex) -> Self:
        return Point(a[0], a[1], a[2])

    def __add__(self, op):
        if isinstance(op, Vector):
            return Point.fromarray(self.asarray + op.asarray)
        else:
            return NotImplemented

    def __sub__(self, op):
        if type(op) == Point:
            return Vector.fromarray(self.asarray - op.asarray)
        else:
            return NotImplemented

    def __eq__(self, op) -> bool:
        if type(op) == Point:
            return (self.asarray == op.asarray).all()
        else:
            return NotImplemented


class Vector(Point):
    def __eq__(self, op) -> bool:
        return NotImplemented


class Arc(Vector):
    pass


class Path(MutableSequence):
    pass


class Move(Vector):
    pass


class Trip(MutableSequence):
    pass
