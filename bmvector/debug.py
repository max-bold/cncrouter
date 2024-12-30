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


np.set_printoptions(precision=3, suppress=True)

j = 50000
a = 5000
v = 1000
vin = 15
vout = 378
p = 6500

# # ts = np.zeros(7,float)
js = np.array((1, 0, -1, 0, -1, 0, 1)) * j
# # ts= pr.calcspeedramp()

t = time()
# try:
# ts = pr.plan5(j, a, v, p, vin, vout)
# except Exception as ex:
#     print(f"{ex}")
# else:
t = time() - t

# print(ts, f"t= {t*1000:.3f} ms")

# # ts = np.array((0.1, 0.2, 0.1, 3, 0.15, 0.1, 0.15), float)
# # ts = np.array([0.09325, 0.0, 0.09325, 0.0, 0.07276, 0.0, 0.07276])
# print(ts)
# print(pr.integratetolist(ts, js, vin))
# # ts += np.array((0.1, 0, 0.1, 0, 0.111479023011, 0, 0.111479023011), float)
# # print(pr.integratetolist(ts, js, vin))

# p= 119.529
# vin= 110.777
# vout=  19.936

tt = time()
fails = 0
medt: float = 0
maxlen = 0
n = 1000000
max_medt = 0
min_medt = float("inf")
for i in range(n):
    vin = np.random.rand() * v
    vout = np.random.rand() * v
    p = np.random.rand() * 1000
    pstr = f"#{i:7g}: {p=:8.3f}, {vin=:8.3f}, {vout=:8.3f}"
    maxlen = max(maxlen, len(pstr))
    if len(pstr) < maxlen:
        for ii in range(maxlen - len(pstr)):
            pstr += " "
    print(f"\r{pstr}, medt={medt*1000:.3f} ms", end="")

    try:
        t = time()
        ts = pr.plan5(j, a, v, p, vin, vout)
        t = time() - t
        medt = medt * 0.99 + t * 0.01
        if i > 100:
            min_medt = min(min_medt, medt)
            max_medt = max(max_medt, medt)
    except pr.PathtoshortError:
        # print(f"{Fore.YELLOW} to short{Fore.RESET}")
        pass
    except Exception as ex:
        print(f' {Fore.RED}failed with: "{ex}"{Fore.RESET}')
        fails += 1
tt = time() - tt
print(
    f"\n{Fore.GREEN}Done {n} calcs in {tt:.3f}s, med time = {min_medt*1000:.3f}-{max_medt*1000:.3f} ms, {Fore.RED}{fails} failed{Fore.RESET}"
)
