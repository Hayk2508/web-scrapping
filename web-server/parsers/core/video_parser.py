from django.db import transaction
from .media_parser import MediaParser
from .enums import Parsers
from . import register_parsers_builder
from ..models import VideoParsedObject, VideoParser as Video_Parser


class VideoParser(MediaParser):

    def __init__(self, url: str, max_videos: int):
        super().__init__(url=url)
        self.max_videos = max_videos

    def parse(self):
        video_parser, _ = Video_Parser.objects.get_or_create(url=self.url)
        video_parsed_objects = []
        video_tags = self.fetch(tag="video")[: self.max_videos]
        video_urls = []
        for video in video_tags:
            video_url = video.find("a")
            if video_url:
                video_url = video_url.get("href")
            else:
                video_url = video.get("src")

            if not video_url.startswith(("http://", "https://")):
                video_url = self.process_url(media_url=video_url)

            video_urls.append(video_url)
        with transaction.atomic():
            for video_url in video_urls:
                video_parsed_object, _ = VideoParsedObject.objects.get_or_create(
                    video_url=video_url, parser=video_parser
                )
                video_parsed_objects.append(video_parsed_object)

        return video_parsed_objects


@register_parsers_builder(Parsers.VIDEOS)
class VideoParserBuilder:
    def __call__(self, url: str, max_videos: int):
        return VideoParser(url=url, max_videos=max_videos)
