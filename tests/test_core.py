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
        self.brew.urls_exist = [
            ('/index.html',),
            ('/myxml.xml', 'xml'),
            ('/myjson.json', 'json'),
        ]
        self.brew_bad = Brew("http://kinkerl.github.com/eukalypse_brew")
        self.brew_bad.urls_exist = [
            ('/myxml.xml', 'xml', 'error'),
        ]
        self.brew_bad.urls_root = ['/index2.html']
        self.brew_bad.urls_sitemap = ['/sitemap_doesnotexist.xml']
        self.brew_bad.urls_robots = ['/robots_doesnotexist.txt']

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
            self.brew._check_exist('/myxml_invalid.xml', 'xml')

    def test_exist_json_invalid(self):
        with self.assertRaises(Exception):
            self.brew._check_exist('/myjson_invalid.json', 'json')

    def test_exist_wrong_content_type(self):
        with self.assertRaises(Exception):
            self.brew._check_exist('/myjson.json', 'xml')

        with self.assertRaises(Exception):
            self.brew._check_exist('/myxml.xml', 'json')

        with self.assertRaises(Exception):
            self.brew._check_exist('/index.html', 'unknown')

    def test_exist_file_not_found(self):
        with self.assertRaises(Exception):
            self.brew._check_exist('/index_not_found.html', 'generic')

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
