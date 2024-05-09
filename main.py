from abc import ABC, abstractmethod
import requests
from bs4 import BeautifulSoup
import os
from urllib.parse import urlparse, urljoin
import argparse
import validators
from parsers.parser_abc import Parser
from parsers.image_parser import ImgParser


def main():
    parser = argparse.ArgumentParser(description='Download images from a webpage.')
    parser.add_argument('-url', '--url', type=str, help='URL of the webpage containing images')
    parser.add_argument('-d', '--directory', type=str, help='Directory to save downloaded images')
    args = parser.parse_args()

    url = args.url
    directory = args.directory

    if url is None or directory is None:
        print("Error: Please provide both URL and directory arguments.")
        return

    if not validators.url(url):
        print("Error: Invalid URL provided.")
        return

    if not os.path.exists(directory):
        os.makedirs(directory)

    img_parser = ImgParser(url=url, directory=directory)
    img_parser.parse()
    print("Images downloaded successfully.")


if __name__ == "__main__":
    main()
