#!/usr/bin/env python3

from linphone import *
import unittest


def func(x):
    return x + 1


class UnittestTest(unittest.TestCase):
    def test(self):
        self.assertEqual(func(3), 4)


class LinphoneTest(unittest.TestCase):
    def setUp(self):
        self.p = Linphone("samus", "secretpasscode", "Gunship", None, None, None)

    def test_lptype(self):
        self.assertEqual(type(self.p), Linphone)

    def tearDown(self):
        self.p.__exit__()

if __name__ == "__main__":
    unittest.main()