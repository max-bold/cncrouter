import numpy as np
import numpy.linalg as la
import math
from pyquaternion import Quaternion
from numbers import Number
from typing import Self, Any, Iterable, Sequence
from nptyping import NDArray, Shape, Float64, DType, Float


class point(np.ndarray):
    def __new__(
        cls, x: int | float | NDArray[Shape["7"], Float], *coords: int | float
    ) -> Self:
        r = np.zeros(7, float).view(cls)
        if not coords and isinstance(x, (np.ndarray, Sequence)):
            r[: len(x)] = x[:]
        else:
            r[0] = x
            r[1 : len(coords) + 1] = coords
        return r

    @staticmethod
    def issequence(op) -> bool:
        for f in ["__getitem__", "__len__"]:
            if f not in dir(op):
                return False
        return True

    def __eq__(self, other):
        if type(other) == point:
            for a, b in zip(self, other):
                if abs(a - b) > 0.0000000001:
                    return False
            return True
        else:
            return False

    def __ne__(self, other):
        return not self.__eq__(other)

    def __sub__(self, other):
        if type(other) == point:
            return vector((self.view(np.ndarray) - other.view(np.ndarray)))
        else:
            raise TypeError(
                f"Unsupported operand type(s) for __sub__: '{type(self).__name__}' and '{type(other).__name__}'"
            )

    @property
    def asarray(self):
        return self.view(np.ndarray)


class vector(point):
    @property
    def norm(self):
        return la.norm(self)

    def to3d(self, unit: bool = False) -> "vector":
        if not unit:
            return vector(self[:3])
        else:
            return vector(self[:3]).tounit()

    @property
    def len(self):
        return la.norm(self[:3])

    def tounit(self) -> "vector":
        return self / self.norm

    def dir(self, *args) -> "vector":
        return self.tounit()

    def rotate(self, axis: "vector", angle: float) -> "vector":
        q = Quaternion(axis=axis[:3], angle=angle)
        rv = q.rotate(self[:3])
        r = vector(self)
        r[:3] = rv
        return r

    def dot(self, v: "vector") -> float:
        return np.dot(self.asarray, v.asarray)

    def angleto(self, v: "vector") -> float:
        return math.acos(self[:3].dot(v[:3]) / self.len / v.len)

    def cross(self, v: "vector") -> "vector":
        return vector((np.cross(self[:3], v[:3])))

    def eval(self, p: float) -> point:
        return point((self * p))

    def __eq__(self, other):
        if type(other) == vector:
            for a, b in zip(self, other):
                if abs(a - b) > 0.0000000001:
                    return False
            return True
        else:
            return False

    def __mul__(self, other) -> "vector":
        if isinstance(other, Number):
            return vector(self.view(np.ndarray) * other)
        else:
            raise TypeError(
                f"Multiplication of {type(self).__name__} by {type(other).__name__} is not supported"
            )

    def __add__(self, other) -> "vector":
        if type(other) == vector or type(other) == arc:
            return vector(self.asarray + other.asarray)
        else:
            raise TypeError(
                f"Adding {type(other).__name__} to {type(self).__name__} is not supported"
            )

    def __truediv__(self, other) -> "vector":
        if isinstance(other, Number):
            return vector(self.asarray / other)
        else:
            raise TypeError(
                f"{type(self).__name__} can be divided only by number, {type(other).__name__} given"
            )

    # __truediv__ = __div__


class arc(vector):
    def __new__(cls, x, *coords, sdir: vector | tuple[float | int]) -> "arc":
        r = super().__new__(cls, x, *coords).view(cls)
        r.sdir = vector(sdir[: min(3, len(sdir))]).tounit()
        return r

    def __array_finalize__(self, obj):
        self.sdir: vector = None

    def fromvar(v: vector, a: vector, r: float) -> "arc":
        gamma = math.acos(v.len / 2 / r) - math.pi / 2
        sv = vector((v.rotate(a, gamma).to3d(unit=True)))
        return arc(v, sdir=sv)

    @property
    def chord(self) -> vector:
        return vector(self[:3])

    @property
    def chordlen(self) -> float:
        return self.chord.norm

    @property
    def radius(self):
        alpha = self.chord.angleto(self.sdir)
        return abs(self.chord.norm / 2 / math.sin(alpha))

    @property
    def len(self):
        return 2 * self.radius * self.chord.angleto(self.sdir)

    @property
    def norm(self):
        return la.norm([self.len] + self[3:].tolist())

    @property
    def angle(self):
        return 2 * self.chord.angleto(self.sdir)

    def dir(self, p: float) -> vector:
        return self.sdir.rotate(
            axis=self.sdir.cross(self), angle=self.angle * p
        ).tounit()

    def eval(self, p: float) -> point:
        ang = self.len * p / self.radius
        axis = self.sdir.cross(self)
        centr = self.sdir.to3d(unit=True).rotate(axis, math.pi / 2) * self.radius
        rv = (centr * -1).rotate(axis, ang)
        res = rv + centr
        res[3:] = (self * p)[3:]
        return point(res)

    @staticmethod
    def fromttr(t1: vector, t2: vector, r=float) -> "arc":
        alpha = t1.angleto(t2)
        beta = alpha - math.pi
        axis = t1.cross(t2)
        cv: vector = t1.to3d(unit=True).rotate(axis, math.pi / 2) * r
        ev = cv.rotate(axis, beta)
        return arc((cv + ev), sdir=t1)

    @staticmethod
    def fillet(t1: vector, t2: vector, r: float) -> tuple[vector, "arc", vector]:
        alpha = t1.angleto(t2)
        trim = r / math.tan(alpha / 2)
        if trim <= t1.len and trim <= t2.len:
            iv = t1 / t1.len * (t1.len - trim)
            ivend = iv.eval(1)
            ov = t2 / t2.len * (t2.len - trim)
            ovstart = (t1 + (t2 / t2.len * trim)).eval(1)
            av = ovstart - ivend
            a = arc(av, sdir=iv.tounit())
            return iv, a, ov
        else:
            raise ValueError(
                f"Length of input vectors must be greater then trim value. Given {t1.len=}, {t2.len=}, {trim=}"
            )

    @staticmethod
    def fbydist(t1: vector, t2: vector, dist: float) -> tuple[vector, "arc", vector]:
        alpha = t1.angleto(t2) / 2
        x = math.sin(alpha / 2)
        r = dist * x / (1 - x)
        return arc.fillet(t1, t2, r)

    @property
    def asvector(self):
        return vector(self.asarray)

    def __eq__(self, other):
        if type(other) == arc:
            return self.asvector == other.asvector and self.sdir == other.sdir
        else:
            raise TypeError(
                f"{type(self).__name__} can't be compared with {type(other).__name__}"
            )

    # def __add__(self, other):
    #     if type(other) == vector:
    #         return vector(self.asarray + other.asarray)
    #     else:
    #         return super().__add__(other)
