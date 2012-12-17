import requests
from lxml import etree
from xml.dom import minidom
from furl import furl
from bs4 import BeautifulSoup


CONTENT_TYPES = {
    'xml': ('text/xml', 'application/rss+xml'),
    'json': ('application/json'),
}


class Brew:

    def __init__(self, base):
        self.sitemap_schema_url = 'http://www.sitemaps.org/schemas/sitemap/0.9/sitemap.xsd'

        self.base = base
        self.switch_homelink = True
        self.urls_root = ['/']
        self.urls_exist = [('/')]
        self.urls_sitemap = ['/sitemap.xml']
        self.urls_robots = ['/robots.txt']

    def _create_url(self, url):
        f = furl(self.base)
        f.path = str(f.path) + url
        return f.url

    def _verify_content_type(self, content_type, key):
        for expected_type in CONTENT_TYPES[key]:
            if expected_type in content_type:
                return True
        return False

    def check_all(self):
        """ find all functions starting with "check_" and call them"""
        #find out the name of the current function so that we can ignore it later
        import inspect
        name_of_current_function = inspect.stack()[0][3]

        for fname in dir(self):
            if fname.startswith('check_') and fname != name_of_current_function:
                f = getattr(self, fname)
                f()

    def check_exist(self):
        """
        urls_exist = [
                ('/generic.html'),
                ('/myxml.xml', 'xml'),
                ('/myjson.json','json')
            ]
        """
        for target in self.urls_exist:
            if len(target) == 2:
                url, urltype = target
            elif len(target) == 1:
                url = target
                urltype = 'generic'
            else:
                raise Exception("unknown urls_exist definition")

            response = requests.get(self._create_url(url))
            if not response.status_code == 200:
                raise Exception("url ({0}) response not 200".format(url))
            if urltype == 'xml':
                #check if valid xml. if not, this will fail
                minidom.parseString(response.content)

                #check if the response content type matches xml
                if not self._verify_content_type(response.headers.get('content-type'), 'xml', url):
                    raise Exception("content-type for url ({0}) is set to ({1}) but should be one of ({2})".format(url, response.headers.get('content-type'), CONTENT_TYPES['xml']))
            elif urltype == 'json':
                # TODO(s@digitalkultur.net) check if valid json in response content

                #check if the response content type matches json
                if not self._verify_content_type(response.headers.get('content-type'), 'json', url):
                    raise Exception("content-type for url ({0}) is set to ({1}) but should be one of ({2})".format(url, response.headers.get('content-type'), CONTENT_TYPES['json']))
            elif urltype == 'generic':
                pass
            else:
                raise Exception("urltype ({0}) not known".format(urltype))

    def check_sitemap(self):
        for url in [self._create_url(url) for url in self.urls_sitemap]:
            response = requests.get(url)
            if not response.status_code == 200:
                raise Exception("sitemap({0}) response not 200".format(url))
            r = requests.get(self.sitemap_schema_url)
            if not r.status_code == 200:
                raise Exception("sitemap schema ({0}) response not 200".format(url))

            if r.status_code == 200:
                xmlschema_doc = etree.XML(r.content)
                xmlschema = etree.XMLSchema(xmlschema_doc)
                xmldoc = etree.XML(response.content)
                if not xmlschema.validate(xmldoc):
                    raise Exception("sitemap does not validate")

            #if the xml is valid but can not get parsed, this will raise an exception
            minidom.parseString(response.content)

    def check_robots(self):
        for url in [self._create_url(url) for url in self.urls_robots]:
            response = requests.get(url)
            if not response.status_code == 200:
                raise Exception("robots({0}) response not 200".format(url))
            for line in response.content.splitlines():
                if not line.startswith(('User-agent: ', 'Disallow: ', 'Allow: ')):
                    raise Exception("robots.txt ({0}) has strange content".format(url))

    def check_homelink(self):
        """ Takes a look at the root urls and the links on them.
        It is expected to have at least 1 link to itself. These links are usually on the Logo.

        If you do not want checks for this homelink to occure, set Brew.switch_homelink to False.
        """
        if not self.switch_homelink:
            return
        for url in [self._create_url(url) for url in self.urls_root]:
            response = requests.get(url)
            if not response.status_code == 200:
                raise Exception("robots({0}) response not 200".format(url))
            soup = BeautifulSoup(response.content)
            a_elements = soup.find_all('a')
            homelink_exists = False
            for a_element in a_elements:
                if a_element.get('href') == url:
                    homelink_exists = True
            if not homelink_exists:
                raise Exception("Link back to Home does not exist on the root pages ({0})".format(url))
