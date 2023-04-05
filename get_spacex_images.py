import argparse
import requests
from work_with_files import safe_images
from work_with_files import define_filetype
from work_with_files import create_folder


def get_spacex_images(id, num_launch=0):
    response = requests.get("https://api.spacexdata.com/v5/launches")
    if not num_launch:
        for element in response.json():
            if element['id'] == id:
                image_urls = element["links"]["flickr"]["original"]
                date = element["date_local"]
                break
        n = 0
        create_folder("Images_spacex")
        for image_url in image_urls:
            safe_images(
                image_url,
                f"Images_spacex\\spacex_{id}_{date[0:10]}_{n}"
                f"{define_filetype(image_url)}"
            )
            n += 1
    else:
        image_urls = response.json()[num_launch]["links"]["flickr"]["original"]
        date = response.json()[num_launch]["date_local"]
        n = 0
        create_folder("Images_spacex")
        for image_url in image_urls:
            safe_images(
                image_url,
                f"Images_spacex\\spacex_{id}_{date[0:10]}_{n}"
                f"{define_filetype(image_url)}"
            )
            n += 1


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
        get_spacex_images(args.id)
    else:
        num_launch = -1
        while True:
            response_dictionary = requests.get(
                "https://api.spacexdata.com/v5/launches"
            ).json()[num_launch]
            if not response_dictionary["links"]["flickr"]["original"]:
                num_launch -= 1
            else:
                last_id = response_dictionary['id']
                break
        get_spacex_images(last_id, num_launch)


if __name__ == "__main__":
    main()
