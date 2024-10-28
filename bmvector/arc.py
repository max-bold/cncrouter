from bmvector.geo2 import Arc, Vector
from math import sqrt, pi
import numpy as np

np.printoptions(precision=2)


a = Arc(sqrt(2), 2 + sqrt(2), 0, r=-2, n=(0, 0, 1))
# a = Arc(1, 1, 0, r=1, n=(0, 0, 1))
with np.printoptions(precision=1, suppress=True, floatmode="fixed"):
    print(a.len/abs(a.r)/pi)
