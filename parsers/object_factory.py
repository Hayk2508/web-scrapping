from .image_parser import ImgParserBuilder
from .video_parser import VideoParserBuilder


class ObjectFactory:
    def __init__(self):
        self.builders = {}

    def register_builder(self, key, builder):
        self.builders[key] = builder

    def create(self, key, **kwargs):
        builder = self.builders.get(key)
        if not builder:
            raise ValueError(key)
        return builder(**kwargs)


def initialize_factory():
    factory = ObjectFactory()
    factory.register_builder('images', ImgParserBuilder())
    factory.register_builder('videos', VideoParserBuilder())
    return factory



