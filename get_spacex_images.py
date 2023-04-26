import argparse
import requests
import os
from work_with_files import save_images
from work_with_files import define_filetype
from pathlib import Path


def get_response_launches():
    response = requests.get(
        "https://api.spacexdata.com/v5/launches"
    )
    response.raise_for_status()
    response_launches = response.json()
    return response_launches


def get_urls_spacex_images_by_id(launch_id):
    response_launches = get_response_launches()
    for launch_inf in response_launches:
        if launch_inf['id'] == launch_id:
            image_urls = launch_inf["links"]["flickr"]["original"]
            date = launch_inf["date_local"]
            break
    return image_urls, date


def get_urls_spacex_images_by_launch_num(launch_num):
    response_launches = get_response_launches()
    image_urls = response_launches[launch_num]["links"]["flickr"]["original"]
    date = response_launches[launch_num]["date_local"]
    return image_urls, date


def get_last_launch_id_with_images():
    launch_num = -1
    response_launches = get_response_launches()
    while True:
        response_launch = response_launches[launch_num]
        if not response_launch["links"]["flickr"]["original"]:
            launch_num -= 1
        else:
            last_id = response_launch['id']
            break
    return last_id, launch_num


def save_all_images(image_urls, date, launch_id):
    os.makedirs('Images_spacex', exist_ok=True)
    for num_image_url, image_url in enumerate(image_urls):
        save_images(
            image_url,
            Path.cwd() / 'Images_spacex' /
            f'spacex_{launch_id}_{date[0:10]}_'
            f'{num_image_url}{define_filetype(image_url)}'
        )


def main():
    parser = argparse.ArgumentParser(
        description="Программа загружает кадры запуска Spacex"
                    " в файл Images_spacex (если нет, создает)"
                    "по ID этого запуска, указывается следующим"
                    " образом: --id ID. Если она не будет указана"
                    " загрузятся фотографии поcледнего запуска, "
                    "для которой есть фотографии, "
    )
    parser.add_argument("--id", help="укажите ID запуска")
    args = parser.parse_args()
    if args.id:
        image_urls, date = get_urls_spacex_images_by_id(args.id)
        save_all_images(image_urls, date, args.id)
    else:
        last_id, launch_num = get_last_launch_id_with_images()
        image_urls, date = get_urls_spacex_images_by_launch_num(launch_num)
        save_all_images(image_urls, date, last_id)


if __name__ == "__main__":
    main()
