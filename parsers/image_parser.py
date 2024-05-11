from .media_parser import MediaParser


class ImgParser(MediaParser):
    def __init__(self, url, directory):
        super().__init__(url=url, directory=directory)

    def parse(self):
        img_tags = self.fetch(tag='img')
        for img in img_tags:
            img_url = img.get('src')
            if not img_url.startswith(('http://', 'https://')):
                img_url = self.process_url(url=img_url)
            self.download(url=img_url)
