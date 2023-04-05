import os
import argparse
import requests
from dotenv import load_dotenv
from work_with_files import safe_images
from work_with_files import define_filetype
from work_with_files import create_folder


load_dotenv()
API = os.environ['API']


def get_APOD(params, day=''):
    url_day_photo = 'https://api.nasa.gov/planetary/apod'
    response = requests.get(
        url_day_photo,
        params=params
    ).json()
    create_folder('Photos_of_the_day')
    if day:
        response = [response]
    for dict_in_list in response:
        url = dict_in_list['hdurl']
        filetype = define_filetype(url)
        date = dict_in_list['date']
        safe_images(
            url,
            f"Photos_of_the_day\\image_for_{date}{filetype}"
        )

def main():
    parser = argparse.ArgumentParser(
        description='Программа скачивает фотографии дня в файл '
                    '"Photos_of_the_day" в рабочей директории, (если нет создает)'
    )
    parser.add_argument("--count", type=int,  help="Укажите количество случайных фотографий")
    parser.add_argument("--day", help="Укажите день, за который нужно получить фото, в формате YYYY-MM-DD")
    parser.add_argument("--days", help="Укажите промежуток дней, за которые хотите получить фотографии, в формате YYYY-MM-DD-YYYY-MM-DD")
    args = parser.parse_args()

    if args.count:
        params = {
            'count': args.count,
            'api_key': API
        }
        get_APOD(params)
    if args.day:
        params = {
            'date': args.day,
            'api_key': API
        }
        get_APOD(params, args.day)
    if args.days:
        params = {
            'start_date': args.days[:10],
            'end_date': args.days[11:],
            'api_key': API
        }
        get_APOD(params)


if __name__ == "__main__":
    main()
