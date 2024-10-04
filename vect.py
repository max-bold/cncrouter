import geo
from math import pi

p = geo.Point(0, -2)
v = geo.Vector(1, 0)
a = geo.Arc(v, p)
print(a.evaluate(a.len/2))
# print(a.isleft)
