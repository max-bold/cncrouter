from math import pi
from pyquaternion import Quaternion

v = (1, 1, 1)
r = (0, 1, 2)
a = -pi/2

q = Quaternion(axis=r,angle=a)
print(q.rotate(v))