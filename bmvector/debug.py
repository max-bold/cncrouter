from bmvector.geo3 import vector, arc, point


# v1 = vector(1, 0, 0, 1, 2, 3, 4)
# v2 = vector(0, 1, 0, 1, 2, 3, 4)
# a = arc.fromttr(v1, v2, 2)
# print(a.eval(0), a.eval(0.5), a.eval(1))

p1 = point(0, 0)
p2 = point(1, 3)
p3 = point(p1)
v = vector(4, 6)
print(v - p2)

reveal_type(point.__new__())
reveal_type(vector.__new__())
reveal_type(arc.__new__())
