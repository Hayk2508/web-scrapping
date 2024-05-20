from .media_parser import MediaParser
from . import register_builder


class VideoParser(MediaParser):

    def __init__(self, url: str, max_videos: int):
        super().__init__(url=url)
        self.max_videos = max_videos

    def parse(self):
        video_tags = self.fetch(tag="video")
        return [
            (
                self.process_url(media_url=video.find("a")["href"])
                if not video.find("a")["href"].startswith(("http://", "https://"))
                else video.find("a")["href"]
            )
            for video in video_tags
        ]


@register_builder("videos")
class VideoParserBuilder:
    def __call__(self, url: str, max_videos: int):
        return VideoParser(url=url, max_videos=max_videos)
