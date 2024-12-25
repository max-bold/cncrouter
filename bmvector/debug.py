# # from geo3 import vector, arc, point
# from math import sin, pi
# import numpy as np

# a = np.linspace(0,1,1)
# b = range(1)
# print(b[0])

import profiler as pr
from time import time
import numpy as np
from colorama import Fore, Style


np.set_printoptions(precision=5, suppress=True)

j = 50000
a = 5000
v = 1000
vin = 50
vout = 200
p = 150000

# # ts = np.zeros(7,float)
js = np.array((1, 0, -1, 0, -1, 0, 1)) * j
# # ts= pr.calcspeedramp()

# t = time()
# try:
ts = pr.plan4(j, a, v, p, vin, vout)
# except Exception as ex:
#     print(f"{ex}")
# else:
# t = time() - t

# print(ts, ts.sum(), t)

# # ts = np.array((0.1, 0.2, 0.1, 3, 0.15, 0.1, 0.15), float)
# # ts = np.array([0.09325, 0.0, 0.09325, 0.0, 0.07276, 0.0, 0.07276])
print(ts)
print(pr.integratetolist(ts, js, vin))
# # ts += np.array((0.1, 0, 0.1, 0, 0.111479023011, 0, 0.111479023011), float)
# # print(pr.integratetolist(ts, js, vin))

# #86548:
# p=143.033
# vin=166.349
# vout=948.6951

# p= 164.307
# vin= 587.996
# vout= 997.926

# tt = time()
# maxt: float = 0
# fails = 0
# medt: float = 0
# maxlen = 0
# n = 10000
# for i in range(n):
#     vin = np.random.rand() * v
#     vout = np.random.rand() * v
#     p = np.random.rand() * 10000
#     pstr = f"#{i:7g}: {p=:8.3f}, {vin=:8.3f}, {vout=:8.3f}"
#     maxlen = max(maxlen, len(pstr))
#     if len(pstr) < maxlen:
#         for ii in range(maxlen - len(pstr)):
#             pstr += " "
#     print(f"\r{pstr} {medt=:.4f}", end="")

#     try:
#         t = time()
#         ts = pr.plan4(j, a, v, p, vin, vout)
#         t = time() - t
#         medt = medt * 0.99 + t * 0.01
#         maxt = max(t, maxt)
#         # print(f"{ts.sum()=} done in {t}s")
#     except pr.PathtoshortError:
#         print(f"{Fore.YELLOW} to short{Fore.RESET}")
#     except Exception as ex:
#         print(f' {Fore.RED}filed with:   "{ex}"{Fore.RESET}')
#         # print("Failed")
#         fails += 1
# tt = time() - tt
# print(
#     f"\n{Fore.GREEN}Done {n} calcs in {tt}s, max time = {maxt}s, med time = {tt/n}, {fails} failed{Fore.RESET}"
# )
