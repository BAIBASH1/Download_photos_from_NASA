from dotenv import load_dotenv
import os
import requests
import datetime
import argparse
import random
from work_with_files import save_images
from pathlib import Path


def get_response_dates(params):
    response = requests.get(
        'https://api.nasa.gov/EPIC/api/natural/all',
        params=params
    )
    response.raise_for_status()
    response_images = response.json()
    return response_images


def get_image_name(date, params):
    response = requests.get(
        f'https://api.nasa.gov/EPIC/api/natural/date/{date}',
        params=params
    )
    response.raise_for_status()
    image_name = response.json()[0]['image']
    return image_name


def get_earth_photo_url(num_date, params):
    response_images = get_response_dates(params)
    str_date = response_images[num_date]['date']
    date = datetime.date.fromisoformat(str_date)
    image_name = get_image_name(date, params)
    url_earth_photo = f'https://api.nasa.gov/EPIC/archive/natural/' \
                      f'{date.strftime("%Y/%m/%d")}/png/{image_name}.png'
    return url_earth_photo, date


def get_num_date(date, params):
    response_dates = get_response_dates(params)
    if "2015-06-12" < date:
        for num_date, element in enumerate(response_dates):
            if element['date'] == date:
                return num_date
        else:
            print("За эту дату нет фотографий")
    else:
        print("Слишком поздняя дата, попробуйте дату раньше")


def get_random_date(counts, params):
    response_dates = get_response_dates(params)
    random_dates = random.sample(response_dates, counts)
    return random_dates


def find_and_save_images(num, params):
    url_earth_photo, date = get_earth_photo_url(num, params)
    os.makedirs('Earth_photos', exist_ok=True)
    save_images(
        url_earth_photo,
        Path.cwd() / 'Earth_photos' / f'earth_photo_{date}.png',
        params=params)


def main():
    load_dotenv()
    nasa_api = os.environ['NASA_API']
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
            find_and_save_images(num, params)
    if args.date:
        num_date = get_num_date(args.date, params)
        find_and_save_images(num_date, params)
    if args.random_count:
        for random_date in get_random_date(args.random_count, params):
            num_date = get_num_date(random_date['date'], params)
            find_and_save_images(num_date, params)


if __name__ == '__main__':
    main()
