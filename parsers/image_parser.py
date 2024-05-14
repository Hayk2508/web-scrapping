from .media_parser import MediaParser
from .object_factory import register_builder


class ImgParser(MediaParser):
    def __init__(self, url, directory):
        super().__init__(url=url, directory=directory)

    def parse(self):
        img_tags = self.fetch(tag="img")
        for img in img_tags:
            img_url = img.get("src")
            if not img_url.startswith(("http://", "https://")):
                img_url = self.process_url(media_url=img_url)
            self.download(media_url=img_url)


@register_builder("images")
class ImgParserBuilder:
    def __call__(self, url: str, directory: str, **_ignored):
        return ImgParser(url=url, directory=directory)
