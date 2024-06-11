from django.contrib.contenttypes.models import ContentType

from . import register_builder
from .media_parser import MediaParser
from ..models import ImageParser, ImageParsedObject


class ImgParser(MediaParser):
    def __init__(self, url):
        super().__init__(url=url)

    def parse(self):
        image_parser, created = ImageParser.objects.get_or_create(url=self.url)

        image_parsed_objects = []

        img_tags = self.fetch(tag="img")

        for img in img_tags:
            img_url = img.get("src")

            if not img_url.startswith(("http://", "https://")):
                img_url = self.process_url(media_url=img_url)

            if not ImageParsedObject.objects.filter(
                image_url=img_url, image_parser=image_parser
            ).exists():
                image_parsed_objects.append(
                    ImageParsedObject(
                        image_url=img_url, obj_type="image", image_parser=image_parser
                    )
                )

        ImageParsedObject.objects.bulk_create(image_parsed_objects)

        return image_parser.image_parsed_objects.all()


@register_builder("images")
class ImgParserBuilder:
    def __call__(self, url: str, **_ignored):
        return ImgParser(url=url)
