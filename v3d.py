from collections.abc import MutableSequence


class Point:
    def __init__(self, x, y, z) -> None:
        self.x = x
        self.y = y
        self.z = z

    def __add__(self,op):
        if type(op)==Vector:
            return Point(self.x+)


class Vector(Point):
    pass


class Arc(Vector):
    pass


class Path(MutableSequence):
    pass


class Move(Vector):
    pass


class Trip(MutableSequence):
    pass
