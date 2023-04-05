import requests
import os
from urllib.parse import urlparse
import datetime
from dotenv import load_dotenv

ID = '5eb87d4affd86e000604b38b'
load_dotenv()
API = os.environ['API']


def safe_images(url, path, params=None):
    filename = path
    with open(filename, 'wb') as file:
        file.write(requests.get(url, params=params).content)


def fetch_spacex_launch(id):
    response = requests.get("https://api.spacexdata.com/v5/launches")

    for element in response.json():
        if element['id'] == id:
            image_urls = element["links"]["flickr"]["original"]
            break
    n = 0
    for image_url in image_urls:
        safe_images(image_url, f"images/spacex_{n}.jpg")
        n += 1


def define_filetype(url):
    url_path = urlparse(url).path
    fyletype = os.path.splitext(url_path)[1]
    return fyletype


def get_photos_of_the_day(count_photo):
    url_day_photo = 'https://api.nasa.gov/planetary/apod'
    params = {
        'count': count_photo,
        'api_key': API
    }

    response = requests.get(
        url_day_photo,
        params=params
    )
    for i in range(count_photo):
        url_day_photo = response.json()[i]['url_day_photo']
        filetype = define_filetype(url_day_photo)
        date = response.json()[i]['date']
        safe_images(
            url_day_photo,
            f"Photos_of_the_day/images_for_{date}{filetype}"
        )


def earth_photo(num_photo):
    params = {
        'api_key': API
    }
    for i in range(num_photo):
        str_date = requests.get(
            'https://api.nasa.gov/EPIC/api/natural/all',
            params=params
        ).json()[i]['date']
        date = datetime.date.fromisoformat(str_date)
        image_name = requests.get(
            f'https://api.nasa.gov/EPIC/api/natural/date/{date}',
            params=params
        ).json()[0]['image']
        url_earth_photo = f'https://api.nasa.gov/EPIC/archive/natural/' \
                          f'{date.strftime("%Y/%m/%d")}/png/{image_name}.png'
        safe_images(
            url_earth_photo,
            f"Earth_photos/earth_photo_{date}.png",
            params
        )
