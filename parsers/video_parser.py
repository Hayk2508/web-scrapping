from .parser_abc import Parser
from bs4 import BeautifulSoup
import requests
import os
from urllib.parse import urlparse, urljoin


class VideoParser(Parser):
    def __init__(self, url: str, directory: str, max_videos):
        super().__init__(url)
        self.directory = directory
        self.max_videos = max_videos

    def download_video(self, video_url):
        video_name = os.path.basename(video_url)
        abs_path = os.path.join(self.directory, video_name)
        with open(abs_path, 'wb') as file:
            file.write(requests.get(video_url).content)

    def parse(self):
        html_content = requests.get(self.url).content
        soup = BeautifulSoup(html_content, 'lxml')
        videos = soup.find_all('video')
        if len(videos) > self.max_videos:
            videos = videos[:self.max_videos]
        for video in videos:
            video_url = video.find("a")['href']
            if not video_url.startswith(('http://', 'https://')):
                base_url = '{uri.scheme}://{uri.netloc}'.format(uri=urlparse(self.url))
                video_url = urljoin(base_url, video_url)
            self.download_video(video_url=video_url)






