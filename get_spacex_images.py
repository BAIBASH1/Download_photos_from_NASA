import argparse
import requests
import os
from work_with_files import safe_images
from work_with_files import define_filetype
from pathlib import Path


def get_urls_spacex_images_by_id(id):
    response = requests.get("https://api.spacexdata.com/v5/launches")
    response.raise_for_status()
    for element in response.json():
        if element['id'] == id:
            image_urls = element["links"]["flickr"]["original"]
            date = element["date_local"]
            break
    return image_urls, date


def get_urls_spacex_images_by_launch_num(launch_num):
    response = requests.get("https://api.spacexdata.com/v5/launches")
    response.raise_for_status()
    image_urls = response.json()[launch_num]["links"]["flickr"]["original"]
    date = response.json()[launch_num]["date_local"]
    return image_urls, date



def get_last_id_with_images():
    launch_num = -1
    while True:
        response = requests.get(
            "https://api.spacexdata.com/v5/launches"
        )
        response.raise_for_status()
        response_dictionary = response.json()[launch_num]
        if not response_dictionary["links"]["flickr"]["original"]:
            launch_num -= 1
        else:
            last_id = response_dictionary['id']
            break
    return last_id, launch_num


def main():
    parser = argparse.ArgumentParser(
        description="Программа загружает кадры запуска Spacex"
                    " в файл Images_spacex (если нет создает)"
                    "по ID этого запуска, указывается следующим"
                    " образом: --id ID. Если она не будет указана"
                    " загрузятся фотографии поледнего запуска, "
                    "для которой есть фотографии, "
    )
    parser.add_argument("--id", help="укажите ID запуска")
    args = parser.parse_args()
    if args.id:
        image_urls, date = get_urls_spacex_images_by_id(args.id)
        os.makedirs('Images_spacex', exist_ok=True)
        for num_image_url, image_url in enumerate(image_urls):
            safe_images(
                image_url,
                Path.cwd() / 'Images_spacex' / f'spacex_{args.id}_{date[0:10]}_{num_image_url}'
                                               f'{define_filetype(image_url)}'
            )
    else:
        last_id, launch_nam = get_last_id_with_images()
        image_urls, date = get_urls_spacex_images_by_launch_num(launch_nam)
        os.makedirs('Images_spacex', exist_ok=True)
        for num, image_url in enumerate(image_urls):
            safe_images(
                image_url,
                Path.cwd() / 'Images_spacex' / f'spacex_{last_id}_{date[0:10]}_{num}'
                                               f'{define_filetype(image_url)}'
            )

if __name__ == "__main__":
    main()
