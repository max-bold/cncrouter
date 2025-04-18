from math import sqrt
import numpy as np
import matplotlib.pyplot as plt


def tplaner(p, v, a):
    ta = min(sqrt(p / a), v / a)
    tv = max(0, (p - ta**2 * a) / v)
    return np.array((ta, tv, ta), float)


def tintegrator(ts: np.ndarray, t, maxa):
    if t < 0:
        a = 0
        v = 0
        p = 0
    if t <= ts[0]:
        a = maxa
        v = maxa * t
        p = maxa * t**2 / 2
    elif t <= ts[0:2].sum():
        a = 0
        v = maxa * ts[0]
        p = maxa * ts[0] ** 2 / 2 + v * (t - ts[0])
    elif t <= ts.sum():
        a = -maxa
        tt = t - ts[0:2].sum()
        v = maxa * ts[0] - maxa * tt
        p = (
            maxa * ts[0] ** 2 / 2
            + maxa * ts[0] * ts[1]
            + maxa * ts[0] * tt
            - maxa * tt**2 / 2
        )
    else:
        a = 0
        v = 0
        p = (
            maxa * ts[0] ** 2 / 2
            + maxa * ts[0] * ts[1]
            + maxa * ts[0] * ts[2]
            - maxa * ts[2] ** 2 / 2
        )
    return a, v, p


def tjplaner(path, minv, acc, maxv):
    ta = (sqrt(path * acc + minv**2) - minv) / acc
    ts = np.zeros(3)
    if ta <= (maxv - minv) / acc:
        ts[0] = ta
        ts[2] = ta
    else:
        ta = (maxv - minv) / acc
        pv = path - acc * ta**2 - 2 * minv * ta
        ts[0] = ta
        ts[1] = pv / maxv
        ts[2] = ta
    return ts


def tjintegrator(ts: np.ndarray, t, minv, acc):
    if t <= 0:
        a = 0
        v = 0
        p = 0
    elif t <= ts[0]:
        a = acc
        v = minv + acc * t
        p = acc * t**2 / 2 + minv * t
    elif t <= ts[:2].sum():
        a = 0
        v = minv + acc * ts[0]
        tt = t - ts[0]
        p = acc * ts[0] ** 2 / 2 + minv * ts[0] + (minv + acc * ts[0]) * tt
    elif t <= ts.sum():
        a = -acc
        tt = t - ts[:2].sum()
        v = minv + acc * ts[0] - acc * tt
        p = (
            acc * ts[0] ** 2 / 2
            + minv * ts[0]
            + (minv + acc * ts[0]) * ts[1]
            + (minv + acc * ts[0]) * tt
            - acc * tt**2 / 2
        )
    else:
        a = 0
        v = 0
        p = (
            acc * ts[0] ** 2 / 2
            + minv * ts[0]
            + (minv + acc * ts[0]) * ts[1]
            + (minv + acc * ts[0]) * ts[2]
            - acc * ts[2] ** 2 / 2
        )
    return a, v, p


def inegrator(t, a, vin, pin):
    v = vin + a * t
    p = vin * t + a * t**2 / 2 + pin
    return a, v, p


def integrateto(ts, t, a, vin):
    aa = [a, 0, -a]
    tt = []
    sumt = 0
    for ct in ts:
        if t > sumt + ct:
            tt.append(ct)
            sumt += ct
        elif t > 0:
            tt.append(t - sumt)
            break
    ac = 0
    vc = vin
    pc = 0
    for a, ti in zip(aa, tt):
        ac, vc, pc = inegrator(ti, a, vc, pc)
    if t < 0 or t > ts.sum():
        ac = 0
        vc = 0
    return ac, vc, pc


def tplaner2(
    p: float,
    v: float,
    a: float,
    vin: float = 0,
    vout: float = 0,
) -> np.ndarray:
    t1 = min((sqrt(2 * a * p + vin**2 + vout**2) / sqrt(2) - vin) / a, (v - vin) / a)
    t3 = t1 + (vin - vout) / a
    t2 = max(0, (p + (t3**2 - 2 * t1 * t3 - t1**2) * a / 2 - (t3 + t1) * vin) / v)
    return np.array((t1, t2, t3), float)


if __name__ == "__main__":
    # maxa = 10000
    # maxv = 1000
    # minv = 20
    # ts = tjplaner(200, minv, maxa, maxv)
    # aa = []
    # vv = []
    # pp = []
    # tt = np.linspace(-0.01, ts.sum() + 0.01, 1000)
    # for t in tt:
    #     a, v, p = integrateto(ts, t, maxa, minv)
    #     aa.append(a)
    #     vv.append(v)
    #     pp.append(p)

    # figure, axis = plt.subplots(3, 2)
    # figure.suptitle(f"Vin/Vout = {minv} mm/s, dT = {(tt[1]-tt[0])*1000:.2f} ms")
    # axis[0, 0].plot(tt, aa)
    # axis[0, 0].title.set_text("Acceleration, mm/s²")
    # axis[1, 0].plot(tt, vv)
    # axis[1, 0].title.set_text("Velocity, mm/s")
    # axis[2, 0].plot(tt, pp)
    # axis[2, 0].title.set_text("Position, mm")

    # dp = []
    # dv = []
    # for i in range(len(tt) - 1):
    #     dt = tt[i + 1] - tt[i]
    #     dp.append((pp[i + 1] - pp[i]) / dt)
    #     dv.append((vv[i + 1] - vv[i]) / dt)

    # axis[0, 1].plot(tt[:-1], dv)
    # axis[0, 1].title.set_text("dV/dT, mm/s²")
    # axis[1, 1].plot(tt[:-1], dp)
    # axis[1, 1].title.set_text("dP/dT, mm/s")
    # axis[2, 1].plot(tt[:-1], pp[:-1])
    # axis[2, 1].title.set_text("Position, mm")

    # # for i in range(len(tt-5)):

    # plt.show()
    np.set_printoptions(precision=5, floatmode="fixed")
    ts = tplaner2(2000, 500, 2000, 100, 20)
    print(ts, np.sum(ts))
    # print(tplaner(1000, 5000, 500))
