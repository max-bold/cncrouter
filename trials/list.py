import numpy as np
from nptyping import NDArray
from typing import Sequence

a = np.array((7, 8.554, 9.123), float)
b = np.zeros(3, int)
c = [1, 2, 3, 45]

b[:] = a[:]

print(isinstance(a, (np.ndarray, Sequence)))
print(isinstance(c, (np.ndarray, Sequence)))

d = ()
if not d:
    print("empty")

def fun(*c):
    if not c:
        print("empty")

fun()