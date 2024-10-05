import geo
from math import pi
from numpy import linspace
import matplotlib.pyplot as plt

# p = geo.Point(0, -2)
# v = geo.Vector(1, 0)
# a = geo.Arc(v, p)
# print(a.evaluate(a.len/2))
# # print(a.isleft)

v1 = geo.Vector(20, 0)
v2 = v1.rotate(15/16*pi)
out = geo.Arc.byttd(v1, v2, 5)
print(out)
s=geo.Point(0,0)
x=[]
y=[]
for v in out:
    for p in linspace(0, v.len,30):
        x.append(v.evaluate(p).x+s.x)
        y.append(v.evaluate(p).y+s.y)
    s+=v


plt.plot(x,y)
plt.plot(out[1].center.x+out[0].end.x,out[1].center.y+out[0].end.y,'o')
ax=plt.gca()
ax.set_aspect('equal')
plt.show()
# print(out)
