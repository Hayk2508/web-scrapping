from parsers.core import register_parsed_objects_builder
from parsers.core.enums import Parsers
from parsers.models import ImageParsedObject, VideoParsedObject


@register_parsed_objects_builder(Parsers.IMAGES)
class ImageParsedObjectBuilder:
    def __call__(self, image_url: str, parser_id, **_ignored):
        return ImageParsedObject(image_url=image_url, parser_id=int(parser_id))


@register_parsed_objects_builder(Parsers.VIDEOS)
class VideoParsedObjectBuilder:
    def __call__(self, video_url: str, parser_id, **_ignored):
        return VideoParsedObject(video_url=video_url, parser_id=int(parser_id))
