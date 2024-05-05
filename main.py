import requests
from bs4 import BeautifulSoup
import os
from urllib.parse import urlparse, urljoin


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
    except FileNotFoundError:
        print("Directory not found.")
    except Exception as e:
        print(f"An error occurred: {e}")


url = input("URL: ")
directory = input("Path to the directory: ")
download_images(url, directory)
