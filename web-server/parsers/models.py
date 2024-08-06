from django.db import models

from core.base_models import TimeStamp
from polymorphic.models import PolymorphicModel
from parsers.core.enums import Parsers


class Parser(TimeStamp, PolymorphicModel):
    url = models.URLField()

    def __str__(self):
        return f"{self.url}, {self.id}"


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

    def __str__(self):
        return f"{self.video_url}, {self.id}"
