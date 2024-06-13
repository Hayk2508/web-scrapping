from django.db import models
from polymorphic.managers import PolymorphicManager

from core.base_models import TimeStamp
from polymorphic.models import PolymorphicModel

from parsers.core.media_parser import Parsers


class Parser(TimeStamp, PolymorphicModel):
    url = models.URLField(unique=True)


class ImageParser(Parser):
    pass


class VideoParser(Parser):
    pass


class ParsedObject(TimeStamp, PolymorphicModel):
    parser = models.ForeignKey(Parser, on_delete=models.CASCADE)


class ImageParsedObject(ParsedObject):
    image_url = models.URLField()

    def to_type(self):
        return Parsers.IMAGES.value

    def to_data(self):
        return {"image_url": self.image_url}


class VideoParsedObject(ParsedObject):
    video_url = models.URLField()

    def to_type(self):
        return Parsers.VIDEOS.value

    def to_data(self):
        return {"video_url": self.video_url}
