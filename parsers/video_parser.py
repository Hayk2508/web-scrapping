from .media_parser import MediaParser
from bs4 import BeautifulSoup
import requests


class VideoParser(MediaParser):
    def __init__(self, url: str, directory: str, max_videos):
        super().__init__(url=url, directory=directory)
        self.max_videos = max_videos

    def parse(self):
        html_content = requests.get(self.url).content
        soup = BeautifulSoup(html_content, 'lxml')
        videos = soup.find_all('video')
        if len(videos) > self.max_videos:
            videos = videos[:self.max_videos]
        for video in videos:
            video_url = video.find("a")['href']
            if not video_url.startswith(('http://', 'https://')):
                video_url = self.process_url(url=video_url)
            self.download(url=video_url)






