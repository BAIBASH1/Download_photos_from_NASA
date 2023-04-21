import os
import argparse
import requests
from dotenv import load_dotenv
from work_with_files import save_images
from work_with_files import define_filetype
from pathlib import Path


def get_APOD(params, day=None):
    url_day_photo = 'https://api.nasa.gov/planetary/apod'
    response = requests.get(
        url_day_photo,
        params=params
    )
    response.raise_for_status()
    os.makedirs('Photos_of_the_day', exist_ok=True)
    response_dictionaries_in_list = response.json()
    if day:
        response_dictionaries_in_list = [response_dictionaries_in_list]
    for dictionary_in_list in response_dictionaries_in_list:
        date = dictionary_in_list['date']
        if dictionary_in_list['media_type'] == "image":
            try:
                url = dictionary_in_list['hdurl']
            except KeyError:
                url = dictionary_in_list['url']
        else:
            print(f'За дату {date} нет изображения')
        filetype = define_filetype(url)
        save_images(
            url,
            Path.cwd() / 'Photos_of_the_day' / f'image_for_{date}{filetype}'
        )


def main():
    load_dotenv()
    nasa_api = os.environ['NASA_API']
    parser = argparse.ArgumentParser(
        description='Программа скачивает фотографии дня в файл '
                    '"Photos_of_the_day" в рабочей директории,'
                    ' (если нет создает)'
    )
    parser.add_argument(
        "--count",
        type=int,
        help="Укажите количество случайных фотографий"
    )
    parser.add_argument(
        "--day",
        help="Укажите день, за который нужно"
             " получить фото, в формате YYYY-MM-DD"
    )
    parser.add_argument(
        "--days",
        help="Укажите промежуток дней, за которые хотите"
             " получить фотографии,"
             " в формате YYYY-MM-DD-YYYY-MM-DD"
    )
    args = parser.parse_args()
    if args.count:
        params = {
            'count': args.count,
            'api_key': nasa_api
        }
        get_APOD(params)
    if args.day:
        params = {
            'date': args.day,
            'api_key': nasa_api
        }
        get_APOD(params, args.day)
    if args.days:
        params = {
            'start_date': args.days[:10],
            'end_date': args.days[11:],
            'api_key': nasa_api
        }
        get_APOD(params)


if __name__ == "__main__":
    main()
