import requests
from urllib.parse import urlparse
import os


def save_images(url, filename, params=None):
    response = requests.get(url, params=params)
    response.raise_for_status()
    with open(filename, 'wb') as file:
        file.write(response.content)


def define_filetype(url):
    url_path = urlparse(url).path
    filetype = os.path.splitext(url_path)[1]
    return filetype
