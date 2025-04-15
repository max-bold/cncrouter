import unittest as ut
import bmvector.fillet as fl
import numpy as np


class fillet_test(ut.TestCase):
    def testfillet1(self):
        v1 = np.array((10, 0, 0), float)
        v2 = np.array((0, 10, 0), float)
        for r, t in zip(
            fl.fillet(v1, v2, 3),
            (
                np.array([5.0, 0.0, 0.0]),
                np.array([5.0, 5.0, 0.0]),
                np.array([0.0, 5.0, 0.0]),
            ),
        ):
            self.assertTrue(np.allclose(r, t), 0.01)

    def testfillet2(self):
        v1 = np.array((10, 0, 0), float)
        v2 = np.array((-10, -1, 0), float)
        for r, t in zip(
            fl.fillet(v1, v2, 3),
            (
                np.array([6.84664409, 0.0, 0.0]),
                np.array([0.01564951, -0.31377064, 0.0]),
                np.array([-6.86229359, -0.68622936, 0.0]),
            ),
        ):
            self.assertTrue(np.allclose(r, t), 0.01)

    def testfillet3(self):
        v1 = np.array((10, 0, 0), float)
        v2 = np.array((10, -1, 0), float)
        for r, t in zip(
            fl.fillet(v1, v2, 3),
            (
                np.array([4.97506219, 0.0, 0.0]),
                np.array([10.02493781, -0.5, 0.0]),
                np.array([5.0, -0.5, 0.0]),
            ),
        ):
            self.assertTrue(np.allclose(r, t), 0.01)

    def testfillet3d(self):
        v1 = np.array((10, 0, -10), float)
        v2 = np.array((0, -10, 10), float)
        for r, t in zip(
            fl.fillet(v1, v2, 3),
            (
                np.array([6.32576539, 0.0, -6.32576539]),
                np.array([3.67423461, -3.67423461, 0.0]),
                np.array([0.0, -6.32576539, 6.32576539]),
            ),
        ):
            self.assertTrue(np.allclose(r, t, 0.01))

    def testarcparam(self):
        v1 = np.array([6.32576539, 0.0, -6.32576539])
        v2 = np.array([3.67423461, -3.67423461, 0.0])
        ap = fl.arcparam(v1, v2)
        self.assertAlmostEqual(ap[0], 3.0000, 3)
        self.assertAlmostEqual(ap[1], 6.2832, 3)
