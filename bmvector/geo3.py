import numpy as np
import numpy.linalg as la
import math
from pyquaternion import Quaternion
from numbers import Number


class point(np.ndarray):
    def __new__(cls, *coords: tuple[float, ...]) -> "point":
        r = np.zeros(7, float).view(cls)
        r[: len(coords)] = coords
        return r

    def __eq__(self, other):
        if type(other) == point:
            for a, b in zip(self, other):
                if abs(a - b) > 0.0000000001:
                    return False
            return True
        else:
            return NotImplemented


class vector(point):
    @property
    def norm(self):
        return la.norm(self)

    def to3d(self, unit: bool = False) -> "vector":
        if not unit:
            return vector(*self[:3])
        else:
            return vector(*self[:3]).tounit()

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
        r = vector(*self)
        r[:3] = rv
        return r

    def dot(self, v: "vector") -> float:
        return np.dot(self, v)

    def angleto(self, v: "vector") -> float:
        return math.acos(self[:3].dot(v[:3] / self.len / v.len))

    def cross(self, v: "vector") -> "vector":
        return vector(*(np.cross(self[:3], v[:3])))

    def eval(self, p: float) -> point:
        return point(*(self * p))

    def __eq__(self, other):
        if type(other) == vector:
            for a, b in zip(self, other):
                if abs(a - b) > 0.0000000001:
                    return False
            return True
        else:
            return NotImplemented


class arc(vector):
    def __new__(cls, *coords, sdir: vector) -> "arc":
        r = super().__new__(cls, *coords).view(cls)
        r.sdir = sdir
        return r

    def __array_finalize__(self, obj):
        self.sdir: vector = None

    def fromvar(v: vector, a: vector, r: float):
        gamma = math.acos(v.len / 2 / r) - math.pi / 2
        sv = vector(*(v.rotate(a, gamma).to3d(unit=True)))
        return arc(*v, sdir=sv)

    @property
    def chord(self) -> vector:
        return vector(*self[:3])

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
        return point(*res)

    @staticmethod
    def fromttr(t1: vector, t2: vector, r=float) -> "arc":
        alpha = t1.angleto(t2)
        beta = alpha - math.pi
        axis = t1.cross(t2)
        cv: vector = t1.to3d(unit=True).rotate(axis, math.pi / 2) * r
        ev = cv.rotate(axis, beta)
        return arc(*(cv + ev), sdir=t1)
