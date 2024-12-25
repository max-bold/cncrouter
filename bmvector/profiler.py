"""
Profiler methods for true s-curve movement planning.
inspired by https://github.com/max-bold/wallplotter/blob/main/profiler.py
© Max Boldyrev, 2024.
"""

# from typing import Generator
# from math import copysign
import numpy as np

# from numbers import Number, Real


def integrate(t, j, ain, vin, pin) -> tuple[float, float, float]:
    a = j * t + ain
    v = j * t**2 / 2 + ain * t + vin
    p = j * t**3 / 6 + ain * t**2 / 2 + vin * t + pin
    return a, v, p


def integrateseq(
    ts: np.ndarray[int, np.dtype[np.floating]],
    js: np.ndarray[int, np.dtype[np.floating]],
    vin: float = 0,
) -> tuple[float, float, float]:
    """Integrates time list to get path end parameters.

    Args:
        mj (float): jerk value
        times (ndarray): list of time intervals to integrate
        vin (float, optional): Speed at start point. Defaults to 0.

    Returns:
        pos, speed, acc (float): integration results at endpont (or when times list will end)
    """
    p: float = 0
    v = vin
    a: float = 0
    for j, t in zip(js, ts):
        # Will stop iterate on last t if t is not full length! Useful for integrating on a part of path!
        a, v, p = integrate(t, j, a, v, p)
    return a, v, p


def integratetolist(ts, js, vin):
    res = np.zeros((8, 3), float)
    res[0] = [0, vin, 0]
    for i in range(7):
        res[i + 1] = integrate(ts[i], js[i], *res[i])
    return res


# def calcerrors(
#     js: np.ndarray[int, np.dtype[np.floating]],
#     ts: np.ndarray[int, np.dtype[np.floating]],
#     tp: float,
#     vin: float,
#     vout: float,
# ) -> tuple[float, float]:
#     """Integrates time intervals and calculates solution errors

#     Args:
#         mj (float): jerk value
#         ts (ndarray): List containing time intervals
#         tp (float): Target position
#         vin (float): Speed at start point
#         tv (float): Speed at end point

#     Returns:
#         tuple[float, float]:
#             0: Position error, m
#             1: Speed error, m/s
#     """
#     a, v, p = integrateseq(js, ts, vin)
#     pe = tp - p
#     ve = vout - v
#     return ve, pe


# def dintegrate(
#     mj: float,
#     ts: ndarray[int, dtype[floating]],
#     dt: float,
#     vin: float = 0,
# ) -> Generator:
#     """Integrates timelist in discrete steps. And returns a generator of lists containing results.

#     Args:
#         times (list[float]): time interval lists
#         timestep (float, optional): Integration step in seconds. Defaults to 1/1000.
#         vin (float, optional): Speed at start point in m/s. Defaults to 0.

#     Returns:
#         list of lists (floats): lists containing:
#             0: time
#             1: position
#             2: speed
#             3: acceleration
#             4: jerk
#     """
#     p: float = 0
#     v: float = vin
#     a: float = 0

#     jerks = [1, 0, -1, 0, -1, 0, 1]

#     for t in arange(0, ts.sum(), dt):
#         for i in range(7):
#             j = jerks[i] * mj
#             if t < ts[: i + 1].sum():
#                 break
#         da = j * dt
#         dv = j * (dt**2) / 2 + a * dt
#         dp = j * (dt**3) / 6 + a * (dt**2) / 2 + v * dt
#         a += da
#         v += dv
#         p += dp
#         yield p, v, a, j, t


# def gs(op: float) -> int:
#     if op >= 0.0:
#         return 1
#     else:
#         return -1


def getjs(
    vin: float, vmax: float, vout: float, j: float
) -> np.ndarray[int, np.dtype[np.floating]]:
    """Calculates jerk values for each segment of path depending on vin, vout and vmax:

    Args:
        vin (float): _description_
        vmax (float): _description_
        vout (float): _description_
        j (float): _description_

    Returns:
        ndarray: List of jerk values for each segment of path
    """
    js = np.zeros(7, float)
    if vmax > vin:
        js[0] = 1
        js[2] = -1
    else:
        js[0] = -1
        js[2] = 1
    if vmax > vout:
        js[4] = -1
        js[6] = 1
    else:
        js[4] = 1
        js[6] = -1
    return js * j


def plan(
    tp: float,
    mj: float,
    ma: float,
    mv: float,
    vin: float = 0,
    vout: float = 0,
    tpe: float = 1 / 100,
    tve: float = 1 / 100,
    tstep: float | None = None,
) -> np.ndarray[int, np.dtype[np.floating]]:
    """Calculates movement plan - a list of 7 time intervals, describing the movement.

    Args:
        tp (float): Distance to move
        mj (float): max jerk
        ma (float): max acceleration
        mv (float): max velocity
        vin (float, optional): Speed at start point, m/s. Defaults to 0.
        vout (float, optional): Speed at end point, m/s. Defaults to 0.
        tpe (float, optional): Target position error. Defaults to 1/100.
        tve (float, optional): Target velocity error. Defaults to 1/100.
        tstep (float, optional): Timestep at start. Defaults to min(ma/mj/10, mv/ma/10). Larger timesteps can cause faster but less accurate results. Smaller causes longer convergence.


    Returns:
        t (list[Float]): List of 7 time intervals, describing the movement
    """
    ts = np.zeros(7, float)

    if not tstep:
        tstep = min(ma / mj / 10, mv / ma / 10)

    # pes = False
    # ves = False
    # osccounter = 0
    # Now lets calculate jerk values for each segment of path depending on vin, vout and mv:

    js = getjs(vin, mv, vout, mj)

    p: float = 0
    v: float = vin

    while abs(p - tp) > tpe or abs(v - vout) > tve:

        # ve, pe = calcerrors(js, ts, tp, vin, vout)
        # v, p = integrateseq(js, ts, vin)[1:]
        avps = integratetolist(js, ts, vin)

        # If oscilation (repeated change of pe sign) is detected we have to reduce tstep to break inf loop.

        # if pes != tp > avps[7, 3] or ves != vout > avps[7, 2]:
        #     osccounter += 1
        #     pes = tp > avps[7, 3]
        #     ves = vout > avps[7, 2]
        # if osccounter > 100:
        #     tstep = tstep / 2
        #     osccounter = 0

        if avps[7, 3] < tp:
            if js[0] > 0 and avps[3, 2] < mv:
                pass
            if js[0] < 0 and avps[3, 2] > mv:
                pass

        # if avps[7, 3] < tp:
        #     # Rise jerk time
        #     v3 = integrateseq(js, ts[:3], vin)[1]
        #     a1 = integrateseq(js, ts[:1], vin)[0]
        #     if abs(a1) < ma:
        #         ts[0] += tstep
        #         ts[2] = ts[0]
        #     # Rise acc time
        #     elif v3 < mv:
        #         ts[1] += tstep
        #     # Rise travel time
        #     else:
        #         ts[3] += tstep

        # elif p > tp:
        #     # Lower travel time
        #     if ts[3] > 0:
        #         ts[3] = max(ts[3] - tstep, 0)
        #     # Lower acc time
        #     elif ts[1] > 0:
        #         ts[1] = max(ts[1] - tstep, 0)
        #     # Lower jerk time
        #     else:
        #         ts[0] = max(ts[0] - tstep, 0)
        #         ts[2] = ts[0]

        # # Lets integrate timelist and calculate errors again to correct vout error
        # v, p = integrateseq(js, ts, vin)[1:]

        # if v > vout:
        #     # Rise neg jerk time
        #     a5 = integrateseq(js, ts[:5], vin)[0]
        #     if abs(a5) < ma:
        #         ts[4] += tstep
        #         ts[6] = ts[4]
        #     # Rise neg acc time
        #     else:
        #         ts[5] += tstep

        # elif v < vout:
        #     # Lower neg acc time
        #     if ts[5] > 0:
        #         ts[5] = max(ts[5] - tstep, 0)
        #     else:
        #         # Lower neg jerk time
        #         ts[4] = max(ts[4] - tstep, 0)
        #         ts[6] = ts[4]

    return ts


def plansimple(j, maxa, maxv, tp, cb=None):
    ts = np.zeros(7, float)
    js = np.array((1, 0, -1, 0, -1, 0, 1), float) * j
    tstep = 1 / 10000
    avps = np.zeros((8, 3), float)
    while avps[7, 2] < tp:
        if avps[1, 0] < maxa:
            ts[0] += tstep
            ts[2] += tstep
            ts[4] += tstep
            ts[6] += tstep
        elif avps[3, 1] < maxv:
            ts[1] += tstep
            ts[5] += tstep
        else:
            ts[3] += tstep
        avps = integratetolist(ts, js, 0)
        if cb:
            cb(avps)
    return ts


def plan2(j, maxa, maxv, tp, vin=0, vout=0, cb=None):
    if vin > maxv or vout > maxv:
        raise ValueError(f"{vin=} and {vout=} must be smaller or equal to {maxv=}!")
    js = np.array((1, 0, -1, 0, -1, 0, 1), float) * j
    ts = np.zeros(7, float)
    avps = integratetolist(ts, js, vin)
    while avps[7, 2] < tp or avps[7, 1] > vout:
        if avps[3, 1] < maxv or avps[7, 1] > vout:
            if avps[3, 1] < maxv:
                if avps[1, 0] < maxa:
                    s = maxa / j / 1000
                    ts[0] += s
                    ts[2] += s
                else:
                    s = maxv / maxa / 1000
                    ts[1] += s
                avps = integratetolist(ts, js, vin)
            if avps[7, 1] > vout:
                if -avps[5, 0] < maxa:
                    s = maxa / j / 1000
                    ts[4] += s
                    ts[6] += s
                else:
                    s = maxv / maxa / 1000
                    ts[5] += s
                avps = integratetolist(ts, js, vin)
        else:
            s = tp / maxv / 1000
            if tp - avps[7, 2] < 10 * maxv * s:
                s = s / 10
            ts[3] += s
            avps = integratetolist(ts, js, vin)
    return ts


class PathtoshortError(Exception):
    def __init__(self, *args):
        super().__init__(*args)


class NoconvergenceError(Exception):
    def __init__(self, *args):
        super().__init__(*args)


def alignspeed(ts, js, vin, vout, maxa, maxv, tvp, s):
    avps = integratetolist(ts, js, vin)
    up = None
    while abs(avps[7, 1] - vout) > tvp:
        if avps[7, 1] < vout:
            if up == False:
                s /= 2
            up = True
            if ts[5] > 0:
                ts[5] = max(ts[5] - s, 0)
            elif ts[4] > 0:
                ts[4] = max(ts[4] - s, 0)
                ts[6] = ts[4]
            elif avps[1, 0] < maxa:
                ts[0] += s
                ts[2] = ts[0]
            elif avps[3, 1] < maxv:
                ts[1] += s
        if avps[7, 1] > vout:
            if up == True:
                s /= 2
            up = False
            if -avps[5, 0] < maxa:
                ts[4] += s
                ts[6] = ts[4]
            else:
                ts[5] += s
        avps = integratetolist(ts, js, vin)
        if s == 0:
            raise NoconvergenceError(f"Failed to align speed for")
    return ts


def plan3(j, maxa, maxv, tp, vin=0, vout=0, cb=None):

    tpp = 1 / 1000
    tvp = 1 / 1000
    tap = 1 / 1000

    if vin > maxv or vout > maxv:
        raise ValueError(f"{vin=} and {vout=} must be smaller or equal to {maxv=}!")
    js = np.array((1, 0, -1, 0, -1, 0, 1), float) * j
    ts = np.zeros(7, float)

    avps = integratetolist(ts, js, vin)

    s = 1 / 100
    up = None

    while abs(avps[7, 1] - vout) > tvp:
        if avps[7, 1] < vout:
            if up == False:
                s /= 2
            up = True
            if ts[5] > 0:
                ts[5] = max(ts[5] - s, 0)
            elif ts[4] > 0:
                ts[4] = max(ts[4] - s, 0)
                ts[6] = ts[4]
            elif avps[1, 0] < maxa:
                ts[0] += min(s, (maxa - avps[1, 0]) / j)
                ts[2] = ts[0]
            else:
                if ts[0]:
                    ts[1] += min(s, (maxv - avps[3, 1]) / ts[0] / j)
                else:
                    ts[1] += s
        elif avps[7, 1] > vout:
            if up == True:
                s /= 2
            up = False
            if ts[1] > 0:
                ts[1] = max(ts[1] - s, 0)
            elif ts[0] > 0:
                ts[0] = max(ts[0] - s, 0)
                ts[2] = ts[0]
            elif -avps[5, 0] < maxa:
                ts[4] += min(s, (maxa + avps[5, 0]) / j)
                ts[6] = ts[4]
            else:
                if ts[3]:
                    ts[5] += min(s, (vout - avps[7, 1]) / ts[3] / j)
                else:
                    ts[5] += s
        avps = integratetolist(ts, js, vin)

        if s == 0:
            raise NoconvergenceError(
                f"Couldn't calculate speed ramp with {vin=}, {vout=}, {maxa=},{maxv=}"
            )

    if avps[7, 2] > tp + tpp:
        raise PathtoshortError(
            f"Path {tp=:.3f} is to short. To ramp from {vin=:.3f} to {vout=:.3f} with given {j=:.0f} and {maxa=:.0f} it should be not shorter than {avps[7,2]:.3f}"
        )

    s = 1 / 100
    up = None

    while abs(avps[7, 2] - tp) > tpp:
        if avps[7, 2] < tp:
            if up == False:
                s /= 2
            up = True
            if avps[1, 0] < maxa and -avps[5, 0] < maxa:
                ts[0] += min(s, (maxa - avps[1, 0]) / j)
                ts[2] = ts[0]
            elif avps[3, 1] < maxv:
                if ts[0]:
                    ts[1] += min(s, (maxv - avps[3, 1]) / ts[0] / j)
                else:
                    ts[1] += s
            else:
                ts[3] += s
        if avps[7, 2] > tp:
            if up == True:
                s /= 2
            up = False
            if ts[3] > 0:
                ts[3] = max(ts[3] - s, 0)
            elif ts[1] > 0:
                ts[1] = max(ts[1] - s, 0)
            elif ts[0] > 0:
                ts[0] = max(ts[0] - s, 0)
                ts[2] = ts[0]
                ss = s * (ts[1] + 2 * ts[0]) / (ts[5] + 2 * ts[4])
                ts[4] = max(ts[4] - ss, 0)
                ts[6] = ts[4]
        ts = alignspeed(ts, js, vin, vout, maxa, maxv, tvp, s)
        avps = integratetolist(ts, js, vin)
        if s == 0:
            raise NoconvergenceError("Failed to adjust path length")

    return ts
