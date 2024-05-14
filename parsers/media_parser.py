import os
from abc import ABC
from urllib.parse import urljoin, urlparse
import requests
from .parser_abc import Parser


class MediaParser(Parser, ABC):

    def __init__(self, url, directory):
        super().__init__(url=url)
        self.directory = directory

    def download(self, media_url: str):
        media_name = os.path.basename(media_url)
        abs_path = os.path.join(self.directory, media_name)
        with open(abs_path, "wb") as file:
            file.write(requests.get(media_url).content)

    def process_url(self, media_url: str):
        base_url = "{uri.scheme}://{uri.netloc}".format(uri=urlparse(self.url))
        return urljoin(base_url, media_url)



