import numpy as np
import numpy.linalg as la
import math
from pyquaternion import Quaternion


class point(np.ndarray):
    def __new__(cls, *coords: tuple[float, ...]) -> "point":
        r = np.zeros(7, float).view(cls)
        r[: len(coords)] = coords
        return r

    def __eq__(self, other):
        if type(other) == point:
            return np.all(self.view(np.ndarray) == other.view(np.ndarray))
        else:
            return NotImplemented


class vector(point):
    @property
    def norm(self):
        return la.norm(self)

    @property
    def to3d(self) -> "vector":
        return np.array(self[:3], float)

    @property
    def len(self):
        return la.norm(self[:3])

    def tounit(self) -> "vector":
        return self / self.norm

    def dir(self, *args) -> "vector":
        return self.tounit()

    def rotate(self, axis: "vector", angle=float) -> "vector":
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
            return np.all(self.view(np.ndarray) == other.view(np.ndarray))
        else:
            return NotImplemented


class arc(vector):
    def __new__(cls, *coords, sdir: vector) -> "arc":
        r = super().__new__(*coords).view(cls)
        r.sdir = sdir
        return r

    def __array_finalize__(self, obj):
        self.sdir: vector = None

    def fromvar(v: vector, a: vector, r: float):
        gamma = math.acos(v.len / 2 / r) - math.pi / 2
        sv = v.rotate(a, gamma)
        return arc(*v, sdir=sv)

    @property
    def chord(self) -> vector:
        return self[:3]

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
    def angle(self):
        return 2 * self.chord.angleto(self.sdir)

    def dir(self, p: float) -> vector:
        self.sdir.rotate(axis=self.cross(self.sdir), angle=self.angle * p)

    def eval(self, p: float) -> point:
        ang = self.len * p / self.radius
        axis = self.sdir.cross(self)
        centr = self.sdir.tounit().rotate(axis, math.pi / 2) * self.radius
        rv = (centr * -1).rotate(axis, ang)
        return point(*(rv + centr))
