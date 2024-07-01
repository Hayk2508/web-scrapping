from django.db import models

from core.base_models import TimeStamp
from polymorphic.models import PolymorphicModel

from parsers.core import register_parsed_objects_builder
from parsers.core.enums import Parsers


class Parser(TimeStamp, PolymorphicModel):
    url = models.URLField()


class ImageParser(Parser):
    pass


class VideoParser(Parser):
    pass


class ParsedObject(TimeStamp, PolymorphicModel):
    parser = models.ForeignKey(Parser, on_delete=models.CASCADE)

    def to_type(self):
        pass

    def to_data(self):
        pass


@register_parsed_objects_builder(Parsers.IMAGES)
class ImageParsedObjectBuilder:
    def __call__(self, image_url: str, parser_id, **_ignored):
        return ImageParsedObject(image_url=image_url, parser_id=int(parser_id))


class ImageParsedObject(ParsedObject):
    image_url = models.URLField()

    def to_type(self):
        return Parsers.IMAGES.value

    def to_data(self):
        return {"image_url": self.image_url}


@register_parsed_objects_builder(Parsers.VIDEOS)
class VideoParsedObjectBuilder:
    def __call__(self, video_url: str, parser_id, **_ignored):
        return VideoParsedObject(video_url=video_url, parser_id=int(parser_id))


class VideoParsedObject(ParsedObject):
    video_url = models.URLField()

    def to_type(self):
        return Parsers.VIDEOS.value

    def to_data(self):
        return {"video_url": self.video_url}
