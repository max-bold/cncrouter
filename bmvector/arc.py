# from bmvector.geo2 import Arc, Vector

# from typing import Iterable, Sequence
# from collections.abc import Sequence

# from math import sqrt, pi
import numpy as np

# np.printoptions(precision=2)


# a = Arc(sqrt(2), 2 + sqrt(2), 0, r=-2, n=(0, 0, 1))
# # a = Arc(1, 1, 0, r=1, n=(0, 0, 1))
# with np.printoptions(precision=1, suppress=True, floatmode="fixed"):
#     print(a.len/abs(a.r)/pi)
# pref = ''
# for c in reversed(Arc.__mro__):
#     print(pref+str(c))
#     pref+=' '

# ar = np.zeros(6, float)
# # print(f"{isinstance(ar,Sequence)=}")
# # # print(*ar.__dir__(), sep="\n")
# print("__len__" in dir(ar))

ar = np.array((1, 2, 3, 4), float)
a2 = [1, 2, 3, 4]
a3 = "1234"
a4 = 1234
# print(' / '.join(ar.tolist()))


def issequence(op) -> bool:
    for f in ["__getitem__", "__len__"]:
        if f not in dir(op):
            return False
    return True


for a in [ar, a2, a3, a4]:
    print(f"{issequence(a)}")
