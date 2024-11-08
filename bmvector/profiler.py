from typing import Generator
from math import copysign
from numpy import zeros, ndarray, dtype, floating, arange


def integrate(
    mj: float,
    ts: ndarray[int, dtype[floating]],
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
    jerks: list[float] = [1, 0, -1, 0, -1, 0, 1]
    p = 0
    v = vin
    a = 0
    for j, t in zip(jerks, ts):
        # Will stop iterrate on last t if t is not full length! Useful for iterratin on a part of path!
        j = mj * j
        da = j * t
        dv = j * (t**2) / 2 + a * t
        dp = j * (t**3) / 3 + a * (t**2) / 2 + v * t
        a += da
        v += dv
        p += dp
    return p, v, a


def calcerrors(
    mj: float,
    ts: ndarray[int, dtype[floating]],
    tp: float,
    vin: float,
    vout: float,
) -> tuple[float, float]:
    """Integrates time intervals and calculates solution errors, also returns total trip time and rms error

    Args:
        mj (float): jerk value
        ts (ndarray): List containing time intervals
        tp (float): Target position
        vin (float): Speed at start point
        tv (float): Speed at end point

    Returns:
        tuple[float, float]:
            0: Position error, m
            1: Speed error, m/s
    """
    p, v, a = integrate(mj, ts, vin)
    ep = tp - p
    ev = vout - v
    return ep, ev


def dintegrate(
    mj: float,
    ts: ndarray[int, dtype[floating]],
    dt: float,
    vin: float = 0,
) -> Generator:
    """Integrates timelist in discrete steps. And returns a generator of lists containing results.

    Args:
        times (list[float]): time interval lists
        timestep (float, optional): Integration step in seconds. Defaults to 1/1000.
        vin (float, optional): Speed at start point in m/s. Defaults to 0.

    Returns:
        list of lists (floats): lists containing:
            0: time
            1: position
            2: speed
            3: acceleration
            4: jerk
    """
    p: float = 0
    v: float = vin
    a: float = 0

    jerks = [1, 0, -1, 0, -1, 0, 1]

    for t in arange(0, ts.sum(), dt):
        for i in range(7):
            j = jerks[i] * mj
            if t < ts[: i + 1].sum():
                break
        da = j * dt
        dv = j * (dt**2) / 2 + a * dt
        dp = j * (dt**3) / 3 + a * (dt**2) / 2 + v * dt
        a += da
        v += dv
        p += dp
        yield p, v, a, j, t


def plan(
    tp: float,
    mj: float,
    ma: float,
    mv: float,
    vin: float = 0,
    vout: float = 0,
    tep: float = 1 / 100,
    tev: float = 1 / 100,
    tstep: float | None = None,
) -> ndarray[int, dtype[floating]]:
    """Calculates movement plan - a list of 7 time intervals, describing the movement.

    Args:
        tp (float): Distance to move
        mj (float): max jerk
        ma (float): max acceleration
        mv (float): max velocity
        vin (float, optional): Speed at start point, m/s. Defaults to 0.
        vout (float, optional): Speed at end point, m/s. Defaults to 0.
        tep (float, optional): Target position error. Defaults to 1/100.
        tev (float, optional): Target speed error. Defaults to 1/100.
        ts (float, optional): Timestep at start. Defaults to min(ma/mj/10, mv/ma/10). Larger timesteps can cause faster but less accurate results. Smaller causes longer convergence.


    Returns:
        t (list[Float]): List of 7 time intervals, describing the movement
        i (int): number of iterations needed to find solution
        time (float): Time needed to find solution, s
    """
    ts = zeros(7, float)
    if not tstep:
        tstep = min(ma / mj / 10, mv / ma / 10)

    ep = tp
    ev = vout - vin
    prevepsign: float = 1
    osccounter = 0
    while abs(ep) > tep or abs(ev) > tev:

        ep, ev = calcerrors(mj, ts, tp, vin, vout)

        # If oscilation (repeated change of ep sign) is detected we have to reduce tstep to break inf loop.
        epsign = copysign(1, ep)
        if epsign != prevepsign:
            osccounter += 1
            prevepsign = epsign
        if osccounter > 100:
            tstep = tstep / 2
            osccounter = 0

        if ep > tep:
            # Rise jerk time
            v3 = integrate(mj, ts[:3], vin)[1]
            if ts[0] < ma / mj and v3 < mv:
                ts[0] += tstep
                ts[2] = ts[0]
            # Rise acc time
            elif v3 < mv:
                ts[1] += tstep
            # Rise travel time
            else:
                ts[3] += tstep

        elif ep < -tep:
            # Lower travel time
            if ts[3] > 0:
                ts[3] = max(ts[3] - tstep, 0)
            # Lower acc time
            elif ts[1] > 0:
                ts[1] = max(ts[1] - tstep, 0)
            # Lower jerk time
            else:
                ts[0] = max(ts[0] - tstep, 0)
                ts[2] = ts[0]

        # Lets integrate timelist and calculate errors again to correct vout error
        ep, ev = calcerrors(mj, ts, tp, vin, vout)
        if ev < -tev:
            # Rise neg jerk time
            if ts[4] < ma / mj:
                ts[4] += tstep
                ts[6] = ts[4]
            # Rise neg acc time
            else:
                ts[5] += tstep

        elif ev > tev:
            # Lower neg acc time
            if ts[5] > 0:
                ts[5] = max(ts[5] - tstep, 0)
            else:
                # Lower neg jerk time
                ts[4] = max(ts[4] - tstep, 0)
                ts[6] = ts[4]

    return ts
