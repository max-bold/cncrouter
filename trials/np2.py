import numpy as np
import numpy.linalg as la
from typing import Sequence, Iterable


def issequence(op) -> bool:
    for f in ["__getitem__", "__len__"]:
        if f not in dir(op):
            return False
    return True


# class point(np.ndarray):
#     def __new__(cls, *coords: tuple[float, ...] | tuple[Sequence]) -> "point":
#         r = np.zeros(7, float).view(cls)
#         if len(coords) == 1 and issequence(coords[0]):
#             r[: len(coords[0])] = coords[0]
#         else:
#             r[: len(coords)] = coords
#         return r

#     def __sub__(self, op: "point") -> "vector":
#         if type(op) == point:
#             return vector(self - op)
#         else:
#             return NotImplemented


# class vector(point):
#     @property
#     def len3d(self):
#         return la.norm(self[:3])


class c(np.ndarray):
    def __new__(cls, *coords, a, b):
        r = np.zeros(7, float).view(cls)
        r[: len(coords)] = coords
        r.a = a
        r.b = b
        return r

    def __array_finalize__(self, obj):
        self.a = None
        self.b = None

    @property
    def norm(self):
        return la.norm(self)


c1 = c(1, 1, a=799, b="rtert")

# print(c1.a, c1.b)
print(c1.norm)
print(c1[:3].norm)
