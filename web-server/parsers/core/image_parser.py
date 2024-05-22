from . import register_builder
from .media_parser import MediaParser


class ImgParser(MediaParser):
    def __init__(self, url):
        super().__init__(url=url)

    def parse(self):
        img_tags = self.fetch(tag="img")
        return [
            (
                img.get("src")
                if img.get("src").startswith(("http://", "https://"))
                else self.process_url(media_url=img.get("src"))
            )
            for img in img_tags
        ]


@register_builder("images")
class ImgParserBuilder:
    def __call__(self, url: str, **_ignored):
        return ImgParser(url=url)
