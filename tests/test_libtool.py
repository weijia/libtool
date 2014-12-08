#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_libtool
----------------------------------

Tests for `libtool` module.
"""
import os

import unittest
import sys
import shutil
from libtool.folder_tool import get_year_month_dir

print sys.path
from libtool.package_utils import include_all_ex



class TestLibtool(unittest.TestCase):

    def setUp(self):
        pass

    def test_something(self):
        #include_all_ex("test")
        folder = get_year_month_dir()
        print folder
        if os.path.exists(folder):
            shutil.rmtree(folder)

    def tearDown(self):
        pass

if __name__ == '__main__':
    unittest.main()