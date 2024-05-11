import requests
from bs4 import BeautifulSoup
from .media_parser import MediaParser


class ImgParser(MediaParser):
    def __init__(self, url, directory):
        super().__init__(url=url, directory=directory)

    def parse(self):
        html_content = requests.get(self.url).text
        soup = BeautifulSoup(html_content, 'lxml')
        img_tags = soup.find_all('img')
        for img in img_tags:
            img_url = img.get('src')
            if not img_url.startswith(('http://', 'https://')):
                img_url = self.process_url(url=img_url)
            self.download(url=img_url)
