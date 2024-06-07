from django.contrib.contenttypes.fields import GenericRelation, GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models


class Date(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Url(Date):
    url = models.URLField(unique=True)


class Parser(Date):
    url = models.ForeignKey(Url, on_delete=models.CASCADE)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey("content_type", "object_id")

    class Meta:
        abstract = True


class ImageParser(Parser):
    pass


class VideoParser(Parser):
    pass


class ParsedObject(Date):

    class Meta:
        abstract = True


class ImageParsedObject(ParsedObject):
    parsed_objects = GenericRelation(
        ImageParser,
        content_type_field="content_type",
        object_id_field="object_id",
        related_query_name="parser",
    )
    image_url = models.URLField()


class VideoParsedObject(ParsedObject):
    parsed_objects = GenericRelation(
        VideoParser,
        content_type_field="content_type",
        object_id_field="object_id",
        related_query_name="parser",
    )
    video_url = models.URLField()
