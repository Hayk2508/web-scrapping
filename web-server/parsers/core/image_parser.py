from . import register_parsers_builder
from .media_parser import MediaParser
from .enums import Parsers
from ..models import ImageParser, ImageParsedObject
from django.db import transaction


class ImgParser(MediaParser):
    def __init__(self, url):
        super().__init__(url=url)

    def parse(self):
        image_parser, _ = ImageParser.objects.get_or_create(url=self.url)
        image_parsed_objects = set()
        image_urls = []
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
            image_urls.append(img_url)
        with transaction.atomic():
            for image_url in image_urls:
                image_parsed_object, _ = ImageParsedObject.objects.get_or_create(
                    image_url=image_url, parser=image_parser
                )
                image_parsed_objects.add(image_parsed_object)
        return image_parsed_objects


@register_parsers_builder(Parsers.IMAGES)
class ImgParserBuilder:
    def __call__(self, url: str, **_ignored):
        return ImgParser(url=url)
