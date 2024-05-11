import os
import argparse
import validators
from parsers.image_parser import ImgParser
from parsers.video_parser import VideoParser


def main():
    parser = argparse.ArgumentParser(description='Download images/videos from a webpage.')
    parser.add_argument('-url', '--url', type=str, help='URL of the webpage containing images/videos')
    parser.add_argument('-d', '--directory', type=str, help='Directory to save downloaded images/videos')
    parser.add_argument('-l', '--limit', type=int, help='Set Limit to downloading videos')
    parser.add_argument('-pt', '--parse_type', type=str, choices=['image', 'video'], help='Type of content to parse ('
                                                                                          'image or video)')

    args = parser.parse_args()
    url = args.url
    directory = args.directory
    parse_type = args.parse_type

    if url is None or directory is None:
        print("Error: Please provide both URL and directory arguments.")
        return

    if not validators.url(url):
        print("Error: Invalid URL provided.")
        return

    if not os.path.exists(directory):
        os.makedirs(directory)

    if parse_type == 'image':
        img_parser = ImgParser(url=url, directory=directory)
        img_parser.parse()
        print("Images downloaded successfully.")

    elif parse_type == 'video':
        if args.limit is None:
            print("Error: Please provide the limit ")
            os.removedirs(directory)
            return
        max_videos = args.limit
        video_parser = VideoParser(url=url, directory=directory, max_videos=max_videos)
        video_parser.parse()
        print("Videos downloaded successfully.")
    else:
        print("Error: Please choose what you want to download: image/video")
        os.removedirs(directory)
        return


if __name__ == "__main__":
    main()
