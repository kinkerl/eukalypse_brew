import requests
from lxml import etree
from xml.dom import minidom


class Brew:

    sitemap_schema_url = 'http://www.sitemaps.org/schemas/sitemap/0.9'

    def __init__(self, domain):
        self.domain = domain
        self.urls_exist = ['/']
        self.urls_sitemap = ['sitemap.xml']
        self.urls_robots = ['robots.txt']

    def _create_url(self, url):
        return self.domain + url

    def check_exist(self):
        for url in self.urls_exist:
            print "check exists: %s" % self._create_url(url)
            response = requests.get(self._create_url(url))
            assert response.status_code is 200

    def check_sitemap(self):
        for url in self.urls_sitemap:
            print "check sitemap: %s" % self._create_url(url)
            response = requests.get(self._create_url(url))
            assert response.status_code is 200
            r = requests.get(self.sitemap_schema_url + '/siteindex.xsd')
            assert r.status_code is 200
            if r.status_code == 200:
                xmlschema_doc = etree.XML(r.content)
                xmlschema = etree.XMLSchema(xmlschema_doc)
                xmldoc = etree.XML(response.content)
                assert xmlschema.validate(xmldoc)
            try:
                minidom.parseString(response.content)
            except:
                assert False

    def check_robots(self):
        for url in self.urls_robots:
            print "check robots: %s" % self._create_url(url)
            response = requests.get(self._create_url(url))
            assert response.status_code is 200
            for line in response.content.splitlines():
                assert line.startswith(('User-agent: ', 'Disallow: ', 'Allow: '))

    def check_all(self):
        """ find all functions starting with "check_" and call them"""
        #find out the name of the current function so that we can ignore it later
        import inspect
        name_of_current_function = inspect.stack()[0][3]

        for fname in dir(self):
            if fname.startswith('check_') and fname != name_of_current_function:
                f = getattr(self, fname)
                f()
