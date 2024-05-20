import os

import requests
import validators
from django.core.management.base import BaseCommand

from core import FACTORY
from core.image_parser import ImgParserBuilder
from core.video_parser import VideoParserBuilder


def download_media_files(directory, media_urls):
    for media_url in media_urls:
        download_media_file(directory=directory, media_url=media_url)


def download_media_file(directory, media_url: str):
    media_name = os.path.basename(media_url)
    abs_path = os.path.join(directory, media_name)
    with open(abs_path, "wb") as file:
        file.write(requests.get(media_url).content)


class Command(BaseCommand):
    help = "Download contents from a webpage."

    def add_arguments(self, parser):
        parser.add_argument(
            "-url",
            "--url",
            type=str,
            help="URL of the webpage containing images/videos",
        )
        parser.add_argument(
            "-d",
            "--directory",
            type=str,
            help="Directory to save downloaded images/videos",
        )
        parser.add_argument(
            "-l", "--limit", type=int, help="Set Limit to downloading videos"
        )
        parser.add_argument(
            "-pt",
            "--parse_type",
            type=str,
            choices=["images", "videos"],
            help="Type of content to parse (images or videos)",
        )

    def handle(self, *args, **options):
        url = options["url"]
        directory = options["directory"]
        limit = options["limit"]
        parse_type = options["parse_type"]

        if url is None or directory is None:
            self.stderr.write("Error: Please provide both URL and directory arguments.")
            return

        if not validators.url(url):
            self.stderr.write("Error: Invalid URL provided.")
            return

        if not os.path.exists(directory):
            os.makedirs(directory)

        parsed_args = {
            "url": url,
            "max_videos": limit,
        }

        parser = FACTORY.create(parse_type, **parsed_args)
        media_urls = parser.parse()
        download_media_files(directory=directory,  media_urls=media_urls)
        self.stdout.write(f"{parse_type.upper()} downloaded successfully")
