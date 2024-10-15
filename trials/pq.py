from math import pi
from pyquaternion import Quaternion

v = (1, 0, 0)
r = (0, 1, 0)
a = -pi/2

q = Quaternion(axis=r,angle=a)
print(q.rotate(v))