import numpy as np
import matplotlib.pyplot as plt
import scipy.signal as ss

a = np.random.uniform(-0.1, 0.1, 1000)
bs = [1, 3, 0, 2]
ii = 0
for b in bs:
    for i in range(ii, ii + 250):
        a[i] = a[i] + b
    ii += 250

plt.plot(a, linewidth=0.2)

c = np.zeros(1000, float)
wind = 100
for i in range(len(a)):
    s = int(max(i - wind / 2, 0))
    e = int(min(i + wind / 2, len(a)))
    c[i] = np.average(a[s:e])

plt.plot(c)

d = ss.savgol_filter(a, wind, 1)
plt.plot(d)

e = ss.wiener(a, wind)
plt.plot(e)

f = np.zeros(1000, float)
s = 0
w2 = 20
for i in range(len(a)):
    s = s * (1 - 1 / w2) + a[i] / w2
    f[i] = s

plt.plot(f)

e = np.zeros(1000, float)
for i in range(1, len(a)):
    dif = abs(a[i] - e[i - 1])
    s = 1 if a[i] >= e[i - 1] else -1
    e[i] = e[i - 1] + min(dif, 0.02) * s
plt.plot(e)


plt.show()
