from collections.abc import MutableSequence
from typing import SupportsIndex, Self, ForwardRef, Iterable
import numpy as np
import numpy.linalg as la
from numbers import Number
from math import acos
from pyquaternion import Quaternion


class Point:
    # val: np.ndarray

    def __init__(self, *args: tuple[tuple[float]] | tuple[float, ...]) -> None:
        self.val = np.zeros(7, float)
        if len(args) == 1 and isinstance(args[0], Iterable):
            self.val[: len(args[0])] = args[0]
        elif len(args) > 1:
            self.val[: len(args)] = args
        else:
            raise ValueError("Not enough of arguments to build a point")

    def __repr__(self):
        return f"p{self.val.tolist()}"

    def __add__(self, op: "Vector") -> "Point":
        if isinstance(op, Vector):
            return Point(self.val + op.val)
        else:
            return NotImplemented

    def __sub__(self, op: "Point") -> "Vector":
        if type(op) == Point:
            return Vector(self.val - op.val)
        else:
            return NotImplemented

    def __eq__(self, op: "Point") -> bool:
        if type(op) == Point:
            return np.all(self.val == op.val)
        else:
            return NotImplemented


class Vector(Point):
    @property
    def norm(self) -> float:
        return la.norm(self.val)

    @property
    def len(self) -> float:
        return self.norm

    def normalized(self) -> "Vector":
        return Vector(self.val / self.norm)

    def getdir(self, *args):
        return self.normalized()

    def rotate(self, v: "Vector", a: float) -> "Vector":
        q = Quaternion(axis=v.val[:3], angle=a)
        return Vector(q.rotate(self.val[:3]))

    def dot(self, v: "Vector") -> float:
        if len(self.val) == len(v.val):
            return np.dot(self.val, v.val)
        else:
            raise ValueError(
                f"Dot product can be calculated only for vectors of same dimension. Given {len(self.val)}d and {len(v.val)}d vectors"
            )

    def cross(self, v: "Vector") -> "Vector":
        if len(self.val) >= 3 and len(v.val) >= 3:
            return np.cross(self.val[0:3], v.val[0:3])
        else:
            raise ValueError(
                "Cross product can be calculated only for 3d (ore more) vectors"
            )

    def angleto(self, v: "Vector") -> float:
        return acos(self.dot(v) / self.norm / v.norm)

    def __add__(self, op: "Vector | Point") -> "Vector":
        if isinstance(op, Vector):
            return Vector(self.val + op.val)
        elif type(op) == Point:
            return op + self
        else:
            return NotImplemented

    def __mul__(self, op: float) -> "Vector":
        return Vector(self.val * op)

    def __sub__(self, op):
        return NotImplemented

    def __eq__(self, op: "Vector") -> bool:
        if type(op) == Vector:
            return np.all(self.val == op.val)
        else:
            return NotImplemented

    def eval(self, p: float) -> Point:
        return Point(self.val * p)

    def evalabs(self, l: float) -> Point:
        return Point(self.normalized().val * l)


class Arc(Vector):
    def __init__(
        self, dir: Vector | tuple[float, ...], end: Point | tuple[float, ...]
    ) -> None:
        if type(dir) == Vector:
            self.dir = dir
        else:
            self.dir = Vector(dir)


class Path(MutableSequence):
    pass


class Move(Vector):
    pass


class Trip(MutableSequence):
    pass
