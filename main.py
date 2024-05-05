import requests
from bs4 import BeautifulSoup
import os
from urllib.parse import urlparse, urljoin
import argparse
import validators


def download_images(url, directory):
    try:
        html_content = requests.get(url).text
        soup = BeautifulSoup(html_content, 'lxml')
        img_tags = soup.find_all('img')
        for img in img_tags:
            img_url = img.get('src')
            if not img_url.startswith(('http://', 'https://')):
                base_url = '{uri.scheme}://{uri.netloc}'.format(uri=urlparse(url))
                img_url = urljoin(base_url, img_url)
            img_name = os.path.basename(img_url)
            abs_path = os.path.join(directory, img_name)
            with open(abs_path, 'wb') as file:
                file.write(requests.get(img_url).content)
    except Exception as e:
        print(f"An error occurred: {e}")


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

    if os.path.exists(directory):
        download_images(url, directory)
    else:
        try:
            os.makedirs(directory)
            download_images(url, directory)
        except Exception as e:
            print(f"Error: Failed to create directory - {e}")


if __name__ == "__main__":
    main()
