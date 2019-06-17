#!python

import requests
from bs4 import BeautifulSoup
from pprint import pprint
import sys


class SearchEngine:
    def __init__(self, url, search_method):
        self.search_engine = url
        self.url = url + search_method
        self.counts = 20
        self.soup = None

    def get_url(self, query):
        res = requests.get(self.url + query)
        try:
            res.raise_for_status()
        except Exception as exc:
            print(exc)
        else:
            self.soup = BeautifulSoup(res.content, 'html.parser')

    def get_text(self, query):
        self.get_url(query)
        names = []
        grab = self.soup.find_all('div', attrs={'class': 'organic__url-text'})
        for bite in grab:
            names.append(bite.text)
        return (names)

    def parse_url(self, query):
        self.get_url(query)
        names = []
        grep = self.soup.find_all('a', attrs={'class': 'link'})
        # for i in grap.find('a'):
        #     print(i)
        for i in grep:
            # print(i.find('a', href=True))
            print(i)
        # print(grap)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        ask = sys.argv[1]
    else:
        ask = "arau"
    luckyHits = SearchEngine("https://yandex.ru", "/search/?text=")
    luckyHits.parse_url("lucky star")
    # list = luckyHits.get_text(ask)
    # for i in list:
    #     print(i)


