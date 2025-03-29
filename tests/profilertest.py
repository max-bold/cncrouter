import bmvector.profiler as pr
import unittest as ut
import numpy as np


class Profiler(ut.TestCase):
    def testintegrator(self):
        j = 20
        a0 = 10
        v0 = 15
        p0 = 30
        a, v, p = pr.integrate(10, j, a0, v0, p0)
        self.assertEqual(a, 210)
        self.assertEqual(v, 1115)
        self.assertAlmostEqual(p, 4013.333, 3)

    # def testlistinegr(self):
    #     vin = 15
    #     ts = np.array([3, 7, 2, 10, 12, 8, 1])
    #     js = np.array([1, 0, -1, 0, -1, 0, 1])*20
    #     a, v, p = pr.integratelist(js, ts, 15)
    #     self.assertEqual(a, -200)
    #     self.assertEqual(v, -2365)
    #     self.assertAlmostEqual(p, 3411.667, 3)
