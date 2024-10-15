import numpy as np
import numpy.linalg as la
from typing import SupportsIndex, Sequence, Iterable

a = np.array((1, 2, 3))
b = np.array((4, 5, 6))
c = np.array((1, 2, 3))
n = 5


def normalize(v: np.ndarray):
    return v / la.norm(v)


class vect(np.ndarray):
    def __new__(cls, *args):
        r = np.asarray(args).view(cls)
        r.text = "hello"
        return r

    def __array_finalize__(self, obj):
        if obj is None:
            return
        self.text = getattr(obj, "text", None)

    @property
    def xyz(self):
        return self[0:3]


v = vect(1, 2, 3, 5, 6)
d = [1, 2]
# for i in range(len(d), 3):
#     d.append(0)
# na=np.asarray(d,float)
# na=na.reshape(3)
# na+=[1,2,0]
na = np.zeros(7, float)
na[: len(d)] = d

print(f"Vrctor sum: {a+b=}")
print(f"Vrctor sub: {b-a=}")
print(f"Vector-scalar mult: {a*n=}")
print(f"Vector-scalr div: {a/n=}")
print(f"Dot product of two vectors: {np.dot(a,b)=}")
print(f"Cross product of two vectors: {np.cross(a, b)=}")
print(f"Norm of vector: {la.norm(a)=}")
print(f"Equity of vectors: {(a==b).all()=} and {(a==c).all()=}")
print(f"Vector normalization: {a/la.norm(a)=}")
print(f"Subclassing ndarray: {v=} {2*v=} type={type(v).__name__}")
print(f"Subclassing ndarray with additional properies: {v.text=}")
print(f"Vector slicing: {v.xyz=}")
print(f"{len(a)=}")
print(f"{np.all(a==[1,2,3])=}")
print(f"{na=}")
print(f"{isinstance(na,Iterable)=}")
print(f"{isinstance(d,Iterable)=}")

# np.all()
