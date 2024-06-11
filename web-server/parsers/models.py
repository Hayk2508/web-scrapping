from django.db import models

from core.base_models import TimeStamp


class Parser(TimeStamp):
    url = models.URLField(unique=True)

    class Meta:
        abstract = True


class ImageParser(Parser):
    pass


class VideoParser(Parser):
    pass


class ParsedObject(TimeStamp):
    obj_type = models.CharField()

    class Meta:
        abstract = True

    def __str__(self):
        return self.obj_type


class ImageParsedObject(ParsedObject):
    image_url = models.URLField()
    image_parser = models.ForeignKey(
        ImageParser, on_delete=models.CASCADE, related_name="image_parsed_objects"
    )


class VideoParsedObject(ParsedObject):
    video_url = models.URLField()
    video_parser = models.ForeignKey(
        VideoParser, on_delete=models.CASCADE, related_name="video_parsed_objects"
    )
