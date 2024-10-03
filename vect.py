import geo
from math import pi

p = geo.Point(1, 1)
v = geo.Vector(100,100)
a = geo.Arc(v, p)
print(v.evaluate(0,True))
