from math import pow, sqrt, sin, cos, pi, acos
from typing import Self, Union
from numbers import Number


def sq(a):
    return pow(a, 2)


class Point:
    def __init__(self, x, y) -> None:
        self.x = x
        self.y = y

    def __eq__(self, op: Self) -> bool:
        return op.x == self.x and op.y == self.y

    def __add__(self, op) -> Self:
        if isinstance(op, Vector):
            return Point(op.x + self.x, op.y + self.y)
        else:
            raise NotImplementedError(f"Type {type(op).__name__} not supported")

    def __sub__(self, op: Self):
        return Vector(self.x - op.x, self.y - op.y)

    __radd__ = __add__

    def __repr__(self) -> str:
        return f"({self.x}, {self.y})"


class Vector(Point):

    @property
    def len(self) -> float:
        return sqrt(sq(self.x) + sq(self.y))

    @property
    def unit(self) -> Self:
        len = self.len
        x = self.x / len
        y = self.y / len
        return Vector(x, y)

    def __add__(self, op: Self | Point):
        if isinstance(op, Vector):
            return Vector(op.x + self.x, op.y + self.y)
        elif isinstance(op, Point):
            return Point(op.x + self.x, op.y + self.y)
        else:
            raise NotImplementedError(f"Type {type(op).__name__} not supported")

    def __mul__(self, op):
        if isinstance(op, Number):
            return Vector(self.x * op, self.y * op)
        else:
            raise NotImplementedError(
                f"Type Vector * {type(op).__name__} not supported"
            )

    __rmul__ = __mul__

    def frompoint(p: Point) -> Self:
        return Vector(p.x, p.y)

    def dotproduct(self, vect: Self) -> float:
        return (self.x * vect.x + self.y * vect.y) / self.len / vect.len

    def anglebetween(self, v: Self) -> float:
        return acos(self.dotproduct(v))

    def rotate(self, a: float) -> Self:
        """Returns vector rotated to left at angle a"""
        x = self.x * cos(a) - self.y * sin(a)
        y = self.y * cos(a) + self.x * sin(a)
        return Vector(x, y)

    @property
    def norm(self) -> Self:
        """Return Vector of unit length and same direction"""
        l = self.len
        return Vector(self.x / l, self.y / l)

    def getnormals(self):
        return self.rotate(pi / 2), self.rotate(-pi / 2)

    @property
    def end(self) -> Point:
        return Point(self.x, self.y)

    def evaluate(self, pos: float, normalized: float = False):
        if not normalized:
            if pos <= self.len:
                return Point(self.norm.x * pos, self.norm.y * pos)
            else:
                raise ValueError("Pos must not excid length of vector")
        else:
            return Point(self.x * pos, self.y * pos)


class Arc(Vector):
    def __init__(self, dir: Vector, end: Point) -> None:
        self.dir = dir.norm
        self.x = end.x
        self.y = end.y

        if dir.dotproduct(Vector.frompoint(end)) == 1:
            raise ValueError("Arc end can't lie on it's direction vector")

    @property
    def chordlen(self):
        return Vector(self.x, self.y).len

    @property
    def radius(self):
        alpha = self.dir.anglebetween(Vector(self.x, self.y))
        return abs(self.chordlen / 2 / sin(alpha))

    @property
    def center(self):
        for normal in self.dir.getnormals():
            if normal.dotproduct(self) > 0:
                return normal.norm * self.radius

    @property
    def len(self):
        return 2 * self.radius * Vector(self.x, self.y).anglebetween(self.dir)

    def evaluate(self, pos: float, normalized: float = False):
        return NotImplementedError
        if not normalized:
            if pos <= self.len:
                a = pos / self.radius
            else:
                raise ValueError("Pos must not exceed length of arc")
        else:
            a = 2 * self.dir.anglebetween(Vector(self.x, self.y)) * pos
