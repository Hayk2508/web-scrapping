import os
import argparse
import validators
from parsers import FACTORY
from parsers.image_parser import ImgParserBuilder
from parsers.video_parser import VideoParserBuilder


def main():
    parser = argparse.ArgumentParser(
        description="Download images/videos from a webpage."
    )
    parser.add_argument(
        "-url", "--url", type=str, help="URL of the webpage containing images/videos"
    )
    parser.add_argument(
        "-d", "--directory", type=str, help="Directory to save downloaded images/videos"
    )
    parser.add_argument(
        "-l", "--limit", type=int, help="Set Limit to downloading videos"
    )
    parser.add_argument(
        "-pt",
        "--parse_type",
        type=str,
        choices=["images", "videos"],
        help="Type of content to parse (" "images or videos)",
    )
    args = parser.parse_args()

    parsed_args = {
        "url": args.url,
        "directory": args.directory,
        "max_videos": args.limit,
    }

    if args.url is None or args.directory is None:
        print("Error: Please provide both URL and directory arguments.")
        return

    if not validators.url(args.url):
        print("Error: Invalid URL provided.")
        return

    if not os.path.exists(args.directory):
        os.makedirs(args.directory)

    parser = FACTORY.create(args.parse_type, **parsed_args)
    parser.parse()
    print(f"{args.parse_type.upper()} downloaded successfully")


if __name__ == "__main__":
    main()
