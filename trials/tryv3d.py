# import sys, os

# sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from .. import bmvectors
p=bmvectors.Point(1,2,3)
v=bmvectors.Vector(4,5,6)

print(p==v)
# import sys

# for path in sys.path:
#     print(path)
print(f'{__name__=}')
print(f'{__file__=}')
print(f'{__package__=}')
