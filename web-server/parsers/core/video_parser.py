from .media_parser import MediaParser, Parsers
from . import register_builder
from ..models import VideoParsedObject, VideoParser as Video_Parser, ParsedObject


class VideoParser(MediaParser):

    def __init__(self, url: str, max_videos: int):
        super().__init__(url=url)
        self.max_videos = max_videos

    def parse(self):
        video_parser, created = Video_Parser.objects.get_or_create(url=self.url)

        video_tags = self.fetch(tag="video")

        for video in video_tags:
            video_url = video.find("a")["href"]
            if not video_url.startswith(("http://", "https://")):
                video_url = self.process_url(media_url=video_url)

            if not VideoParsedObject.objects.filter(
                video_url=video_url, parser=video_parser
            ).exists():
                VideoParsedObject.objects.create(
                    video_url=video_url, parser=video_parser
                )

        return ParsedObject.objects.filter(parser=video_parser)


@register_builder(Parsers.VIDEOS)
class VideoParserBuilder:
    def __call__(self, url: str, max_videos: int):
        return VideoParser(url=url, max_videos=max_videos)
