from .gcodereader import gparser
import numpy as np
from ...bmvector.trapezioid import tplaner
from datetime import timedelta
import matplotlib.pyplot as plt

path = r"trials\gcode\3DBenchy_0.2mm_PLA_MEGA0_1h48m.gcode"
parser = gparser()
queue = parser.parse(path)

maxa = 5000  # mm/s²
aa = np.geomspace(100, 10000, 20)
ts = np.zeros(20, float)
# print(aa,ts)

for i in range(20):
    tt = 0
    ta = 0
    tp = 0
    for move in queue:
        p = np.linalg.norm(move[:3])
        plan = tplaner(p, aa[i], move[7])
        ts[i] += plan.sum() / 3600
        # ta += plan[0] + plan[2]
        # tp += p / 1000


# print(timedelta(seconds=tt), timedelta(seconds=ta), tp)
# print(aa,ts)
plt.plot(aa / 1000, ts)
plt.title("Print time vs max acceleration")
plt.xlabel("Acceleration, m/s²")
plt.ylabel("Print time, hours")
# plt.xscale("log", base=2)
plt.grid()
plt.show()
