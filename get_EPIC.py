from dotenv import load_dotenv
import os
import requests
import datetime
import argparse
import random
from work_with_files import safe_images
from work_with_files import create_folder


load_dotenv()
API = os.environ['API']


def earth_photo(num_date):
    str_date = requests.get(
        'https://api.nasa.gov/EPIC/api/natural/all',
        params=params
    ).json()[num_date]['date']
    date = datetime.date.fromisoformat(str_date)
    image_name = requests.get(
        f'https://api.nasa.gov/EPIC/api/natural/date/{date}',
        params=params
    ).json()[0]['image']
    url_earth_photo = f'https://api.nasa.gov/EPIC/archive/natural/' \
                      f'{date.strftime("%Y/%m/%d")}/png/{image_name}.png'
    create_folder('Earth_photos')
    safe_images(
        url_earth_photo,
        f"Earth_photos/earth_photo_{date}.png",
        params=params)


def get_by_date(date):
    dates_response = requests.get(
        'https://api.nasa.gov/EPIC/api/natural/all',
        params=params
    ).json()
    n = 0
    if "2015-06-12" < date:
        for element in dates_response:
            if element['date'] == date:
                earth_photo(n)
                break
            n += 1
        else:
            print("За эту дату нет фотографий")
    else:
        print("Слишком поздняя дата, попробуйте дату раньше")



def main():
    global params
    params = {
        'api_key': API
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
            earth_photo(num)
    if args.date:
        get_by_date(args.date)
    if args.random_count:
        dates_response = requests.get(
            'https://api.nasa.gov/EPIC/api/natural/all',
            params=params
        ).json()
        random_dates = random.sample(dates_response, args.random_count)
        for random_date in random_dates:
            get_by_date(random_date['date'])


if __name__ == '__main__':
    main()
