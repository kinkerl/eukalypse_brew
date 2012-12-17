#!/usr/bin/env python
from eukalypse_brew import Brew
import sys
if sys.version_info < (2, 7):
    import unittest2 as unittest
else:
    import unittest
from mock import patch


class MyBrewTest(unittest.TestCase):

    def setUp(self):
        self.brew = Brew("http://kinkerl.github.com/eukalypse_brew")
        self.brew.url_exist = [
            ('index.html'),
            ('myxml.xml', 'xml'),
            ('myjson.json', 'json'),
        ]
        self.brew_bad = Brew("http://isodontexistabc.com/")

    @patch.object(Brew, 'check_sitemap')
    @patch.object(Brew, 'check_robots')
    @patch.object(Brew, 'check_exist')
    @patch.object(Brew, 'check_homelink')
    def test_checkall(self, mock_homelink, mock_exist, mock_robots, mock_sitemap):
        self.brew.check_all()

        mock_sitemap.assert_called_with()
        mock_robots.assert_called_with()
        mock_exist.assert_called_with()
        mock_homelink.assert_called_with()

    def test_exist_success(self):
        self.brew.check_exist()

    def test_sitemap_success(self):
        self.brew.check_sitemap()

    def test_robots_success(self):
        self.brew.check_robots()

    def test_homelink_success(self):
        self.brew.check_homelink()

    def test_exist_xml_invalid(self):
        with self.assertRaises(Exception):
            self.brew._check_exist('myxml_invalid.xml', 'xml')

    def test_exist_json_invalid(self):
        with self.assertRaises(Exception):
            self.brew._check_exist('myjson_invalid.json', 'json')

    def test_exist_failure(self):
        with self.assertRaises(Exception):
            self.brew_bad.check_exist()

    def test_sitemap_failure(self):
        with self.assertRaises(Exception):
            self.brew_bad.check_sitemap()

    def test_robots_failure(self):
        with self.assertRaises(Exception):
            self.brew_bad.check_robots()

    def test_homelink_failure(self):
        with self.assertRaises(Exception):
            self.brew_bad.check_homelink()
