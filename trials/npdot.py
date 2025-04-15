import numpy as np

v1 = np.array((10, 0, 0))
v2 = np.array((0, 10, 0))

print(np.dot(v1, -v1))
print(np.dot(v1, v1))
print(np.dot(v1, v2))
