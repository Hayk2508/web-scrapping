from django.contrib.contenttypes.models import ContentType

from . import register_builder
from .media_parser import MediaParser
from ..models import Url, ImageParser, ParsedObject, ImageParsedObject


class ImgParser(MediaParser):
    def __init__(self, url):
        super().__init__(url=url)

    def parse(self):
        self.create_url()
        url_website = Url.objects.get(url=self.url)
        image_parsed_objects = set()
        img_tags = self.fetch(tag="img")
        for img in img_tags:
            img_url = img.get("src")
            if not img.get("src").startswith(("http://", "https://")):
                self.process_url(media_url=img.get("src"))
            image_parser = ImageParser.objects.create(
                url=url_website,
                content_type=ContentType.objects.get_for_model(ImageParsedObject),
            )
            if not ImageParsedObject.objects.filter(image_url=img_url).exists():
                parsed_object = ImageParsedObject.objects.create(image_url=img_url)
                image_parser.content_object = parsed_object
                image_parser.save()
            else:
                parsed_object = ImageParsedObject.objects.get(image_url=img_url)
            image_parsed_objects.add(parsed_object)
        return image_parsed_objects


@register_builder("images")
class ImgParserBuilder:
    def __call__(self, url: str, **_ignored):
        return ImgParser(url=url)
