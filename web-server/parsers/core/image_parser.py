from . import register_builder
from .media_parser import MediaParser, Parsers
from ..models import ImageParser, ImageParsedObject, Parser, ParsedObject


class ImgParser(MediaParser):
    def __init__(self, url):
        super().__init__(url=url)

    def parse(self):
        image_parser, created = ImageParser.objects.get_or_create(url=self.url)
        img_tags = self.fetch(tag="img")
        for img in img_tags:
            img_url = img.get("src")

            if not img_url:
                potential_attributes = ["data-src", "srcset"]
                for attr in potential_attributes:
                    img_url = img.get(attr)
                    if attr == "srcset":
                        img_url = img_url.split(",")[0].split()[0]
                    if img_url:
                        break
            if not img_url.startswith(("http://", "https://")):
                img_url = self.process_url(media_url=img_url)

            if not ImageParsedObject.objects.filter(
                image_url=img_url, parser=image_parser
            ).exists():
                ImageParsedObject.objects.create(image_url=img_url, parser=image_parser)

        return ParsedObject.objects.filter(parser=image_parser)


@register_builder(Parsers.IMAGES)
class ImgParserBuilder:
    def __call__(self, url: str, **_ignored):
        return ImgParser(url=url)
