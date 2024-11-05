from geo3 import vector, arc
import numpy.linalg as la

v1 = vector(40, 15, 10, 1, 2, 3, 4)
# v2 = vector(0, 1, 0, 1, 2, 3, 4)
# a = arc.fromttr(v1, v2, 2)
# print(a.eval(0), a.eval(0.5), a.eval(1))
print(la.norm([la.norm(v1[:3])]+v1[3:].tolist()))
print(la.norm(v1))
