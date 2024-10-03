from time import time
from math import pow

s = time()
a = 158

for i in range(1000000):
    b = pow(a, 2)

print(b, time() - s)
