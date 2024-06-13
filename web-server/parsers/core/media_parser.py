import os
from abc import ABC
from urllib.parse import urljoin, urlparse
import requests
from bs4 import BeautifulSoup
from django.forms import model_to_dict
from enum import Enum
from .parser_abc import Parser


class Parsers(Enum):
    IMAGES = "images"
    VIDEOS = "videos"


class MediaParser(Parser, ABC):

    def __init__(self, url):
        super().__init__(url=url)

    def process_url(self, media_url: str):
        base_url = "{uri.scheme}://{uri.netloc}".format(uri=urlparse(self.url))
        return urljoin(base_url, media_url)

    def fetch(self, tag: str):
        html_content = requests.get(self.url).content
        soup = BeautifulSoup(html_content, "html.parser")
        return soup.find_all(tag)
