#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_libtool
----------------------------------

Tests for `libtool` module.
"""

import unittest
import sys
print sys.path
from libtool.package_utils import include_all_ex



class TestLibtool(unittest.TestCase):

    def setUp(self):
        pass

    def test_something(self):
        include_all_ex("test")

    def tearDown(self):
        pass

if __name__ == '__main__':
    unittest.main()