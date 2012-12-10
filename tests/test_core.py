#!/usr/bin/env python
from eukalypse_brew import Brew
import unittest


class MyBrewTest(unittest.TestCase):
    def setUp(self):
        self.brew = Brew("http://www5.mercedes-benz.com/")

    def test_sitemap(self):
        self.brew.check_sitemap()

    def test_robots(self):
        self.brew.check_robots()
