from abc import ABC, abstractmethod

import requests
from bs4 import BeautifulSoup


class Parser(ABC):

    def __init__(self, url):
        self.url = url

    @abstractmethod
    def parse(self):
        pass

    def fetch(self, tag: str):
        html_content = requests.get(self.url).content
        soup = BeautifulSoup(html_content, 'lxml')
        return soup.find_all(tag)
