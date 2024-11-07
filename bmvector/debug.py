from geo3 import vector, arc, point
from math import sin, pi

v1 = vector(10, 0, 0, 6)
v2 = vector(0, 10, 0, 8)
vt1, a, vt2 = arc.fbydist(v1, v2, 1)

print(a.radius)

alpha = pi / 2
print(sin(alpha / 2) / (1 - sin(alpha / 2)))
