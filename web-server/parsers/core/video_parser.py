from django.contrib.contenttypes.models import ContentType

from .media_parser import MediaParser
from . import register_builder
from ..models import VideoParsedObject, VideoParser as Video_Parser


class VideoParser(MediaParser):

    def __init__(self, url: str, max_videos: int):
        super().__init__(url=url)
        self.max_videos = max_videos

    def parse(self):
        video_parser, created = Video_Parser.objects.get_or_create(url=self.url)

        video_tags = self.fetch(tag="video")
        video_parsed_objects = []

        for video in video_tags:
            video_url = video.find("a")["href"]
            if not video_url.startswith(("http://", "https://")):
                video_url = self.process_url(media_url=video_url)

            video_parsed_objects.append(
                VideoParsedObject(
                    video_url=video_url, obj_type="video", video_parser=video_parser
                )
            )

        VideoParsedObject.objects.bulk_create(video_parsed_objects)
        return video_parser.video_parsed_objects.all()


@register_builder("videos")
class VideoParserBuilder:
    def __call__(self, url: str, max_videos: int):
        return VideoParser(url=url, max_videos=max_videos)
