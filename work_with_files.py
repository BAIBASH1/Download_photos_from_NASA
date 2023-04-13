import requests
from urllib.parse import urlparse
import os




def safe_images(url, path, params=None):
    filename = path
    with open(filename, 'wb') as file:
        file.write(requests.get(url, params=params).content)


def define_filetype(url):
    url_path = urlparse(url).path
    filetype = os.path.splitext(url_path)[1]
    return filetype
