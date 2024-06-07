from django.contrib.contenttypes.models import ContentType

from .media_parser import MediaParser
from . import register_builder
from ..models import VideoParsedObject


class VideoParser(MediaParser):

    def __init__(self, url: str, max_videos: int):
        super().__init__(url=url)
        self.max_videos = max_videos

    def parse(self):
        video_parser = VideoParser.objects.create(
            url=self.url,
            content_type=ContentType.objects.get_for_model(VideoParsedObject),
        )
        video_parsed_objects = set()
        video_tags = self.fetch(tag="video")
        for video in video_tags:
            video_url = video.find("a")["href"]
            if not video_url.startswith(("http://", "https://")):
                video_url = self.process_url(media_url=video_url)
            if not VideoParsedObject.objects.filter(video_url=video_url):
                parsed_object = VideoParsedObject.objects.create(video_url=video_url)
                video_parser.content_object = parsed_object
                video_parser.save()
            else:
                parsed_object = VideoParsedObject.objects.get(video_url=video_url)
            video_parsed_objects.add(parsed_object)
        return video_parsed_objects


@register_builder("videos")
class VideoParserBuilder:
    def __call__(self, url: str, max_videos: int):
        return VideoParser(url=url, max_videos=max_videos)
