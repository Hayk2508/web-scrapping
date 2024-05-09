import os
from urllib.parse import urlparse, urljoin
import requests
from bs4 import BeautifulSoup
from .parser_abc import Parser


class ImgParser(Parser):
    def __init__(self, url, directory):
        super().__init__(url)
        self.directory = directory

    def parse(self):
        html_content = requests.get(self.url).text
        soup = BeautifulSoup(html_content, 'lxml')
        img_tags = soup.find_all('img')
        for img in img_tags:
            img_url = img.get('src')
            if not img_url.startswith(('http://', 'https://')):
                base_url = '{uri.scheme}://{uri.netloc}'.format(uri=urlparse(self.url))
                img_url = urljoin(base_url, img_url)
            self.download_image(img_url=img_url)

    def download_image(self, img_url: str):
        img_name = os.path.basename(img_url)
        abs_path = os.path.join(self.directory, img_name)
        with open(abs_path, 'wb') as file:
            file.write(requests.get(img_url).content)



