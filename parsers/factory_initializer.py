from .image_parser import ImgParserBuilder
from .video_parser import VideoParserBuilder
from .object_factory import ObjectFactory


def initialize_factory():
    factory = ObjectFactory()
    factory.register_builder('images', ImgParserBuilder())
    factory.register_builder('videos', VideoParserBuilder())
    return factory
