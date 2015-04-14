#!/usr/bin/env python3
###############################################################################
#
# Connects to the C standard library to do fast(er) random number
# generation.  Preliminary results show at least a 2x speedup with
# no loss of randomness.
#
# Unit test for this module
#
# Author: Braxton Schafer <braxton.schafer@gmail.com> (bjs)
# Organization: Ripon College
#
# Date Created: 13/4/15
#
# Changelog:
#
###############################################################################

import unittest
import fastrand


class TestRandom(unittest.TestCase):

    def test_roll(self):
        self.assertTrue(0 < fastrand.roll() < 7)

    def test_choice(self):
        test_list = ["spam", "eggs", "foo", "bar"]
        self.assertTrue(fastrand.choice(test_list) in test_list)

    def test_shuffle(self):
        test_list = ["spam", "eggs", "foo", "bar"]
        orig = test_list
        self.assertFalse(fastrand.shuffle(test_list) == orig)


if __name__ == '__main__':
    unittest.main()