#!/usr/bin/env python
from eukalypse_brew import Brew
import unittest
from mock import MagicMock


class MyBrewTest(unittest.TestCase):

    def setUp(self):
        self.brew = Brew("http://www5.mercedes-benz.com/")
        self.brew_bad = Brew("http://isodontexistabc.com/")

    def test_checkall(self):
        brew = Brew("http://www5.mercedes-benz.com/")
        brew.check_sitemap = MagicMock()
        brew.check_robots = MagicMock()
        brew.check_exist = MagicMock()

        brew.check_all()

        brew.check_sitemap.assert_called_with()
        brew.check_robots.assert_called_with()
        brew.check_exist.assert_called_with()

    def test_exist_success(self):
        self.brew.check_exist()

    def test_sitemap_success(self):
        self.brew.check_sitemap()

    def test_robots_success(self):
        self.brew.check_robots()

    def test_exist_failure(self):
        try:
            self.brew_bad.check_exist()
        except:
            pass
        else:
            # else should not happen. there should be an error
            # and this else block should be skipped
            self.assertTrue(False)

    def test_sitemap_failure(self):
        try:
            self.brew_bad.check_sitemap()
        except:
            pass
        else:
            # else should not happen. there should be an error
            # and this else block should be skipped
            self.assertTrue(False)

    def test_robots_failure(self):
        try:
            self.brew_bad.check_robots()
        except:
            pass
        else:
            # else should not happen. there should be an error
            # and this else block should be skipped
            self.assertTrue(False)
