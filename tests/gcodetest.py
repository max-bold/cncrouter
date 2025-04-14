import unittest as ut
from trials.gcode.gcodereader import gparser
import numpy as np


class parser_test(ut.TestCase):
    def testnormal(self):
        line = "G1 X107.815 Y108.209 E-.1715"
        p = gparser()
        d = p.comtodict(line)
        self.assertDictEqual(d, {"com": "G1", "x": 107.815, "y": 108.209, "e": -0.1715})

    def testcommainparam(self):
        line = "G1 X107,815 Y108,209 E-,1715"
        p = gparser()
        d = p.comtodict(line)
        self.assertDictEqual(d, {"com": "G1", "x": 107.815, "y": 108.209, "e": -0.1715})

    def testlowercom(self):
        line = "g1 X107.815"
        p = gparser()
        d = p.comtodict(line)
        self.assertDictEqual(d, {"com": "G1", "x": 107.815})

    def testzerosincom(self):
        line = "G001 X107.815"
        p = gparser()
        d = p.comtodict(line)
        self.assertDictEqual(d, {"com": "G1", "x": 107.815})
        line = "G00 X50"
        d = p.comtodict(line)
        self.assertDictEqual(d, {"com": "G0", "x": 50})
        line = "G90"
        d = p.comtodict(line)
        self.assertEqual(d["com"], "G90")

    def testnoval(self):
        line = "G28 X"
        p = gparser()
        d = p.comtodict(line)
        self.assertDictEqual(d, {"com": "G28", "x": None})

    def testlowerparam(self):
        line = "G1 x107.815"
        p = gparser()
        d = p.comtodict(line)
        self.assertDictEqual(d, {"com": "G1", "x": 107.815})

    def testmodal(self):
        lines = ["G1 X100", "Y200"]
        p = gparser()
        for line in lines:
            d = p.comtodict(line)
        self.assertDictEqual(d, {"com": "G1", "y": 200})

    def testmodalerror(self):
        line = "X107.815"
        p = gparser()
        self.assertRaises(ValueError, p.comtodict, line)

    def testtextdispl(self):
        line = "M117 Hello world!"
        p = gparser()
        d = p.comtodict(line)
        self.assertDictEqual(d, {"com": "M117", "text": "Hello world!"})

    def testotvectabs(self):
        line = "G1 X10 Y20 E30"
        p = gparser()
        p.cpos = np.array((5, 5, 5, 5, 5, 5, 5))
        p.cspeed = 500
        res = np.array((5, 15, 0, 0, 0, 0, 25, 500))
        pos = np.array((10, 20, 5, 5, 5, 5, 30))
        d = p.comtodict(line)
        self.assertTrue(np.array_equal(p.dicttovector(d), res))
        self.assertTrue(np.array_equal(p.cpos, pos))

    def testtovectrel(self):
        line = "G1 X10 Y20 E30 F300"
        p = gparser()
        p.cpos = np.array((5, 5, 5, 5, 5, 5, 5))
        p.absextrude = False
        p.absmove = False
        res = np.array((10, 20, 0, 0, 0, 0, 30, 300))
        pos = np.array((15, 25, 5, 5, 5, 5, 35))
        d = p.comtodict(line)
        self.assertTrue(np.array_equal(p.dicttovector(d), res))
        self.assertTrue(np.array_equal(p.cpos, pos))

    def testsetcpos(self):
        line = "G92 X10 Y20"
        p = gparser()
        d = p.comtodict(line)
        p.setcpos(d)
        res = np.array((10, 20, 0, 0, 0, 0, 0))
        self.assertTrue(np.array_equal(p.cpos, res))

    def testhome(self):
        line = "G28 X Y50"
        p = gparser()
        d = p.comtodict(line)
        p.homepos = np.array((200, 0, 0, 0, 0, 0, 0))
        p.hspeed = 200
        p.cpos = np.array((100, 30, 0, 0, 0, 0, 0))
        res = np.array((100, 20, 0, 0, 0, 0, 0, 200))
        m = p.dicttohome(d)
        self.assertTrue(np.array_equal(m, res))
        self.assertEqual(p.cpos[0], p.homepos[0])
        self.assertEqual(p.cpos[1], p.homepos[1] + 50)

    def testparser(self):
        path = r"trials\gcode\3DBenchy_0.2mm_PLA_MEGA0_1h48m.gcode"
        p = gparser()
        pos = p.cpos[:7]
        queue = p.parse(path)
        for move in queue:
            pos += move[:7]
        res = [0.00, 200.00, 48.50, 0.00, 0.00, 0.00, 4251.94]
        self.assertTrue(np.allclose(pos, res, atol=0.01), pos)
