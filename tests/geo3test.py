from bmvector.geo3 import point, vector, arc
import unittest as ut
import math
import numpy as np


class point_test(ut.TestCase):
    def testnew(self):
        p = point(0, 2, 3, 4, 8, 9)
        self.assertEqual(p[3], 4)
        self.assertTrue(type(p) == point)

    def testeq(self):
        p1 = point(0, 1, 2, 3)
        p2 = point(0, 1, 2, 3)
        p3 = point(4, 5, 7)
        v = vector(0, 1, 2, 3)
        self.assertTrue(p1 == p2)
        self.assertFalse(p1 == p3)
        self.assertFalse(p1 == v)


class vector_test(ut.TestCase):
    def testnew(self):
        v = vector(1, 2, 3)
        self.assertEqual(v[2], 3)
        self.assertEqual(type(v), vector)
        self.assertEqual(v[4], 0)

    def testnorm(self):
        v = vector(1, 2, 3, 4, 5)
        self.assertEqual(v.norm, math.sqrt(55))

    def testlen(self):
        v = vector(1, 2, 3, 4, 5)
        self.assertEqual(v.len, math.sqrt(14))

    def testunit(self):
        v = vector(1, 2, 3, 4, 5)
        a = np.array((1, 2, 3, 4, 5)) / math.sqrt(55)
        self.assertEqual(v.tounit(), vector(*a))

    def testdir(self):
        v = vector(1, 2, 3, 4, 5)
        a = np.array((1, 2, 3, 4, 5)) / math.sqrt(55)
        self.assertEqual(v.tounit(), vector(*a))

    def testrotate(self):
        v = vector(1, 0, 0, 2, 3, 4, 5)
        axis = vector(0, 0, 1)
        ang = math.pi / 2
        rv = vector(0, 1, 0, 2, 3, 4, 5)
        self.assertAlmostEqual(sum(v.rotate(axis, ang) - rv), 0)

    def testeq(self):
        v1 = vector(1, 2, 3, 4, 5, 6, 7)
        v2 = vector(1, 2, 3, 4, 5, 6, 7)
        v3 = vector(1, 2, 3, 4, 6, 6, 7)
        p = point(1, 2, 3, 4, 5, 6, 7)
        self.assertTrue(v1 == v2)
        self.assertFalse(v1 == v3)
        self.assertFalse(v1 == p)

    def testdot(self):
        v1 = vector(1, 0, 0)
        v2 = vector(1, 1, 0)
        self.assertAlmostEqual(v1.dot(v2), math.cos(math.pi / 4) * v1.norm * v2.norm)

    def testangleto(self):
        v1 = vector(1, 0, 0)
        v2 = vector(1, 1, 0)
        self.assertAlmostEqual(v1.angleto(v2), math.pi / 4)

    def testcross(self):
        v1 = vector(1, 0, 0)
        v2 = vector(1, 1, 0)
        rv = vector(0, 0, 1)
        self.assertEqual(vector.cross(v1, v2), rv)

    def testeval(self):
        v = vector(2, 2)
        self.assertEqual(v.eval(0.5), point(1, 1))
