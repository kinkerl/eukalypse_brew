import requests
from bs4 import BeautifulSoup


class Github:

    readme_locator = "#readme .entry-content"

    def __init__(self, user, project):
        self.user = user
        self.project = project

    def _create_url(self, path=None):
        return "http://github.com/{0}/{1}/".format(self.user, self.project)

    def check_readme(self, path=None):
        """If path is not set, root path is used"""
        response = requests.get(self._create_url(path))
        if not response.status_code == 200:
            raise Exception("url ({0}) response not 200".format(self._create_url(path)))
        soup = BeautifulSoup(response.content)
        a_elements = soup.find(id="readme").find_all('a')
        img_elements = soup.find(id="readme").find_all('img')
        for a_element in a_elements:
            link = a_element.get('href')
            if not link.startswith('#') and not link == self._create_url(path):
                response = requests.get(link)
                if not response.status_code == 200:
                    raise Exception("url ({0}) response {1}".format(link,response.status_code))

        for img_element in img_elements:
            link = a_element.get('src')
            response = requests.get(link)
            if not response.status_code == 200:
                raise Exception("url ({0}) response is {1}".format(link,response.status_code))

        raise Exception("ar")
