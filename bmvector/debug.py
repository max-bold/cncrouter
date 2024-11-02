from geo3 import vector, arc

v1 = vector(1, 0, 0, 1, 2, 3, 4)
v2 = vector(0, 1, 0, 1, 2, 3, 4)
a = arc.fromttr(v1, v2, 2)
print(a.eval(0), a.eval(0.5), a.eval(1))
