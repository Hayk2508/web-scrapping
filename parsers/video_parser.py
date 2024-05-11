from .media_parser import MediaParser


class VideoParser(MediaParser):
    def __init__(self, url: str, directory: str, max_videos):
        super().__init__(url=url, directory=directory)
        self.max_videos = max_videos

    def parse(self):
        video_tags = self.fetch(tag='video')
        if len(video_tags) > self.max_videos:
            video_tags = video_tags[:self.max_videos]
        for video in video_tags:
            video_url = video.find("a")['href']
            if not video_url.startswith(('http://', 'https://')):
                video_url = self.process_url(url=video_url)
            self.download(url=video_url)






