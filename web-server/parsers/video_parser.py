from .media_parser import MediaParser
from . import register_builder


class VideoParser(MediaParser):

    def __init__(self, url: str, directory: str, max_videos: int):
        super().__init__(url=url, directory=directory)
        self.max_videos = max_videos

    def parse(self, download_content):
        video_tags = self.fetch(tag="video")

        if not download_content:
            return [video.find("a")["href"] for video in video_tags]

        if len(video_tags) > self.max_videos:
            video_tags = video_tags[: self.max_videos]

        for video in video_tags:
            video_url = video.find("a")["href"]
            if not video_url.startswith(("http://", "https://")):
                video_url = self.process_url(media_url=video_url)
            self.download(media_url=video_url)


@register_builder("videos")
class VideoParserBuilder:
    def __call__(self, url: str, directory: str, max_videos: int):
        return VideoParser(url=url, directory=directory, max_videos=max_videos)
