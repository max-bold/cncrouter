import numpy as np

a = np.array((1, 5, 8), float)
b = np.array((0, 3, 1), float)
c = 454
# with np.errstate(divide="ignore"):
#     print((a / b).min())
# p = *a+c
print(type(*a))
