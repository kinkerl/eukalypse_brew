#!/usr/bin/env python
from eukalypse_brew import Github
import unittest


class MyBrewGithubTest(unittest.TestCase):

    def setUp(self):
        self.github = Github("kinkerl", "eukalypse_brew")

    def test_check_readme(self):
        self.github.check_readme()
