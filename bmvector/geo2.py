from collections.abc import MutableSequence
from typing import SupportsIndex, Self, ForwardRef, Iterable
import numpy as np
import numpy.linalg as la
from numbers import Number
from math import acos, asin, pi
from pyquaternion import Quaternion


class Point:

    def __init__(
        self, *args: tuple[tuple[float, ...], ...] | tuple[float, ...]
    ) -> None:
        self.val = np.zeros(7, float)
        if len(args) == 1 and isinstance(args[0], Iterable):
            self.val[: len(args[0])] = args[0]
        elif len(args):
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
    def __init__(self, *args):
        if len(args) == 1 and type(args[0]) == Vector:
            super().__init__(args[0].val)
        else:
            super().__init__(*args)

    @property
    def norm(self) -> float:
        return la.norm(self.val)

    @property
    def len3d(self) -> float:
        return la.norm(self.val[:3])

    @property
    def v3d(self) -> "Vector":
        return Vector(self.val[:3])

    def normalized(self) -> "Vector":
        return Vector(self.val / self.norm)

    def getdir3d(self, *args):
        return Vector(self.val[:3] / la.norm(self.val[:3]))

    def rotate3d(self, v: "Vector", a: float) -> "Vector":
        q = Quaternion(axis=v.val[:3], angle=a)
        return Vector(list(q.rotate(self.val[:3])) + self.val[3:].tolist())

    def dot3d(self, v: "Vector") -> float:
        return np.dot(self.val[:3], v.val[:3])

    def cross3d(self, v: "Vector") -> "Vector":
        return Vector(np.cross(self.val[:3], v.val[:3]))

    def angleto3d(self, v: "Vector") -> float:
        return acos(self.dot3d(v) / self.len3d / v.len3d)

    def __add__(self, op: "Vector | Point") -> "Vector":
        if type(op) == Vector:
            return Vector(self.val + op.val)
        elif type(op) == Point:
            return op + self
        else:
            return NotImplemented

    def __mul__(self, op: float) -> "Vector":
        return Vector(self.val * op)

    def __sub__(self, op: "Vector") -> "Vector":
        if type(op) == Vector:
            return Vector(self.val - op.val)
        else:
            return NotImplemented

    def __eq__(self, op: "Vector") -> bool:
        if type(op) == Vector:
            return np.all(self.val == op.val)
        else:
            return NotImplemented

    def eval(self, p: float) -> Point:
        return Point(self.val * p)

    def __repr__(self):
        return f"v{self.val.tolist()}"


class Arc(Vector):
    def __init__(
        self, *args: Vector | tuple[float, ...], sdir: Vector | tuple[float, ...]
    ) -> None:
        super().__init__(*args)
        self.sdir = Vector(sdir)

    @staticmethod
    def fromvnr(v: Vector, n: Vector, r: float) -> "Arc":
        gamma = acos(v.len3d / 2 / r) - pi / 2
        sv = v.rotate3d(n, gamma)
        return Arc(v, sdir=sv)

    @property
    def chord3d(self) -> Vector:
        return Vector(self.val[:3])

    @property
    def chordlen3d(self) -> float:
        return self.len3d

    @property
    def radius(self) -> float:
        return abs(self.r)

    @property
    def len3d(self) -> float:
        ang = 2 * asin(self.chordlen3d / 2 / self.r)
        if ang < 0:
            ang += pi * 2
        return abs(self.r) * ang

    @property
    def centr(self) -> Point:
        gamma = acos(self.chordlen3d / 2 / abs(self.r))
        d = self.chord3d.normalized().rotate3d(self.n, gamma)
        return Point(d.val * abs(self.r))

    def eval(self, p: float) -> Point:
        """_summary_

        Args:
            p (float): 0 >= p >= 1

        Returns:
            Point: _description_
        """
        pass

    def getdir(self, *args):
        pass

    def __repr__(self):
        return f"a{self.val.tolist()}, r={self.r}"


class Path(MutableSequence):
    pass


class Move(Vector):
    pass


class Trip(MutableSequence):
    pass
