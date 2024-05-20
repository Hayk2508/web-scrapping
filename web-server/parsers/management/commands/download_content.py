import os
import validators
from django.core.management.base import BaseCommand

from core import FACTORY
from core.image_parser import ImgParserBuilder
from core.video_parser import VideoParserBuilder


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
            "directory": directory,
            "max_videos": limit,
        }

        parser = FACTORY.create(parse_type, **parsed_args)
        parser.parse(download_content=True)
        self.stdout.write(f"{parse_type.upper()} downloaded successfully")
