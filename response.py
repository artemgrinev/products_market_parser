import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from settings import proxy_key


class Response:
    __proxy_key = proxy_key
    url = ""

    def get_soup(self):
        r = requests.get(self.url, headers={'User-Agent': UserAgent().chrome}).text
        soup = BeautifulSoup(r)
        return soup

    def proxy_zyte(self):
        proxy_host = "proxy.zyte.com"
        proxy_port = "8011"
        proxy_auth = self.__proxy_key  # Make sure to include ':' at the end
        proxies = {"https": "http://{}@{}:{}/".format(proxy_auth, proxy_host, proxy_port),
                   "http": "http://{}@{}:{}/".format(proxy_auth, proxy_host, proxy_port)}
        r = requests.get(self.url, proxies=proxies, verify=False).text
        soup = BeautifulSoup(r)
        return soup
