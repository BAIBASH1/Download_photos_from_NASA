from dotenv import load_dotenv
import os
import requests
import datetime
import argparse
import random
from work_with_files import safe_images
from pathlib import Path


def get_earth_photo_url(num_date):
    response = requests.get(
        'https://api.nasa.gov/EPIC/api/natural/all',
        params=params
    )
    response.raise_for_status()
    str_date = response.json()[num_date]['date']
    date = datetime.date.fromisoformat(str_date)
    response = requests.get(
        f'https://api.nasa.gov/EPIC/api/natural/date/{date}',
        params=params
    )
    response.raise_for_status()
    image_name = response.json()[0]['image']
    url_earth_photo = f'https://api.nasa.gov/EPIC/archive/natural/' \
                      f'{date.strftime("%Y/%m/%d")}/png/{image_name}.png'
    return url_earth_photo, date

def get_by_date(date):
    dates_response = requests.get(
        'https://api.nasa.gov/EPIC/api/natural/all',
        params=params
    )
    dates_response.raise_for_status()
    if "2015-06-12" < date:
        for num_date, element in enumerate(dates_response.json()):
            if element['date'] == date:
                return num_date
                break
        else:
            print("За эту дату нет фотографий")
    else:
        print("Слишком поздняя дата, попробуйте дату раньше")


def get_random_date(counts):
    dates_response = requests.get(
        'https://api.nasa.gov/EPIC/api/natural/all',
        params=params
    )
    dates_response.raise_for_status()
    random_dates = random.sample(dates_response.json(), counts)
    return random_dates


def main():
    load_dotenv()
    nasa_api = os.environ['NASA_API']
    global params
    params = {
        'api_key': nasa_api
    }
    parser = argparse.ArgumentParser(
        description='Программа скачивает фотографии земли в файл '
                    '"Earth_photos" в рабочей директории, (если нет создает)'
    )
    parser.add_argument(
        '--count',
        type=int,
        help="Укажите количество фотографий, программа выведет"
             " указанное количество последних фотографий"
    )
    parser.add_argument(
        '--date',
        help='Укажите дату в формате YYYY-MM-DD, '
             'программа выведет фото этого дня, если оно есть'
    )
    parser.add_argument(
        '--random_count',
        type=int,
        help='Если нужно сколько-то рандомных фотографий, '
             'нужно ввести число'
    )
    args = parser.parse_args()
    if args.count:
        for num in range(args.count):
            url_earth_photo, date = get_earth_photo_url(num)
            os.makedirs('Earth_photos', exist_ok=True)
            safe_images(
                url_earth_photo,
                Path.cwd() / 'Earth_photos' / f'earth_photo_{date}.png',
                params=params)
    if args.date:
        num_date = get_by_date(args.date)
        url_earth_photo, date = get_earth_photo_url(num_date)
        os.makedirs('Earth_photos', exist_ok=True)
        safe_images(
            url_earth_photo,
            Path.cwd() / 'Earth_photos' / f'earth_photo_{date}.png',
            params=params)
    if args.random_count:
        for random_date in get_random_date(args.random_count):
            num_date = get_by_date(random_date['date'])
            url_earth_photo, date = get_earth_photo_url(num_date)
            os.makedirs('Earth_photos', exist_ok=True)
            safe_images(
                url_earth_photo,
                Path.cwd() / 'Earth_photos' / f'earth_photo_{date}.png',
                params=params)


if __name__ == '__main__':
    main()
