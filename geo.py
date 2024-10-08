from math import pow, sqrt, sin, cos, pi, acos, tan
from typing import Self
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
        if type(op) == Point:
            return Vector(self.x - op.x, self.y - op.y)
        else:
            raise NotImplementedError

    __radd__ = __add__

    def __repr__(self) -> str:
        return f"p({self.x:.2f}, {self.y:.2f})"


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

    def evaluate(self, pos: float):
        return Point(self.norm.x * pos, self.norm.y * pos)

    def __repr__(self):
        return f"v({self.x:.2f}, {self.y:.2f})"


class Arc(Vector):
    def __init__(self, dir: Vector, end: Point) -> None:
        self.dir = dir.norm
        self.x = end.x
        self.y = end.y

        if dir.dotproduct(Vector.frompoint(end)) == 1:
            raise ValueError("Arc end can't lie on it's direction vector")

    def byttr(
        iv: Vector, ov: Vector, radius: float, trim: bool = False
    ) -> Self | tuple[Vector, Self, Vector]:
        """Filets two vectors with an Arc of given radius

        Args:
            iv (Vector): First vector
            ov (Vector): Second vector
            radius (float): Radius of arc
            trim (bool, optional): If True returns a tuple of two vectors separated by arc else returns only arc. Defaults to False.

        Raises:
            ValueError: If vectors are too short to be trimmed by arc and trim is true will raise a ValueError

        Returns:
            Self | tuple[Vector,Self, Vector]: Return depends on trim.
        """
        d = 1 if iv.rotate(pi / 2).dotproduct(ov) > 0 else -1
        c = (iv.norm.rotate(pi / 2 * d) * radius).end
        end = c + (ov.norm.rotate(pi / 2 * -d) * radius)
        a = Arc(iv, end)
        if not trim:
            return a
        else:
            tl = tan(a.inangle / 2) * a.radius
            if iv.len > tl and ov.len > tl:
                v1 = iv.norm * (iv.len - tl)
                v2 = ov.norm * (ov.len - tl)
                return v1, a, v2
            else:
                raise ValueError("Vectors too short to trim")

    def byttd(iv: Vector, ov: Vector, dist: float) -> tuple[Vector, Self, Vector]:
        """Filets two vectors with fixed distance from corner (end of first vector) to arc\n
        r = dist * cos(a / 2) / (1 - cos(a / 2))\n
        where a is angle between vectors and r is arc radius

        Args:
            iv (Vector): First vector
            ov (Vector): Second vector
            dist (float): distance from end of first vector to triming arc

        Returns:
            tuple[Vector, Arc , Vector]: Returns two tlmed vectors separated by Arc
        """
        a = iv.anglebetween(ov)
        r = dist * cos(a / 2) / (1 - cos(a / 2))
        return Arc.byttr(iv, ov, r, True)

    @property
    def chordlen(self):
        return self.chord.len

    @property
    def radius(self):
        alpha = self.dir.anglebetween(self.chord)
        return abs(self.chordlen / 2 / sin(alpha))

    @property
    def center(self):
        for normal in self.dir.getnormals():
            if normal.dotproduct(self) > 0:
                return normal.norm * self.radius

    @property
    def len(self):
        return 2 * self.radius * self.chord.anglebetween(self.dir)

    @property
    def chord(self):
        return Vector(self.x, self.y)

    @property
    def isleft(self):
        n = self.dir.rotate(pi / 2)
        return n.dotproduct(self.chord) > 0

    @property
    def isright(self):
        return not self.isleft

    def evaluate(self, pos: float):
        a = pos / self.radius
        c = self.center
        v = Vector(-c.x, -c.y)
        if self.isright:
            a = -a
        rv = v.rotate(a).end
        return Point(rv.x + c.x, rv.y + c.y)

    @property
    def inangle(self):
        return 2 * self.dir.anglebetween(self.chord)

    def __repr__(self):
        return f"a(r{self.radius:.2f}, a{self.inangle/pi:.2f}pi)"
