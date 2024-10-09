# import sys, os

# sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from .. import v3d
p=v3d.Point(1,2,3)
v=v3d.Vector(4,5,6)

print(p==v)
# import sys

# for path in sys.path:
#     print(path)
print(f'{__name__=}')
print(f'{__file__=}')
print(f'{__package__=}')
