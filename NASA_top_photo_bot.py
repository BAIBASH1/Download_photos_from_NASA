import telegram
import os
import argparse
import time
import random
from pytimeparse import parse
from dotenv import load_dotenv


def open_and_send_image(path, bot, tg_chat_id):
    with open(path, 'rb') as document:
        bot.send_document(
            chat_id=tg_chat_id,
            document=document
        )


def try_send(path, bot, tg_chat_id):
    while True:
        try:
            open_and_send_image(path, bot, tg_chat_id)
            return
        except telegram.error.NetworkError:
            time.sleep(10)


def main():
    load_dotenv()
    tg_token = os.environ['TG_TOKEN']
    tg_chat_id = os.environ['TG_CHAT_ID']
    parser = argparse.ArgumentParser(
        description='Бот присылает фотографии из указанной директории'
                    '(дефолтно равен Photos_of_the_day),'
                    ' с указанным периодом (дефолтно период равен 4ем часам),'
                    ' если фотографии закончатся,'
                    ' начнет случайном порядке присылать фотографии'
    )
    parser.add_argument(
        '--directory',
        default='Photos_of_the_day',
        help='Укажите путь к папке из которой'
             ' необходимо присылать фотографии')
    parser.add_argument('--period',
                        default='4h',
                        help='Укажите период между отправками сообщений,'
                             ' в формате число + текст, например:'
                             ' 12s (равно 12 сек);'
                             ' 1.2h2m1c (равно 1.2*60*60+2*60+1=4441 сек);'
                             ' 1day (равно 86400). '
                             'Дефолтно период равен 4-ем часам'
                        )
    args = parser.parse_args()
    bot = telegram.Bot(token=tg_token)
    paths = [entry for entry in os.scandir(args.directory)]
    period = parse(args.period)
    while True:
        for path in paths:
            try_send(path, bot, tg_chat_id)
            time.sleep(period)
        random.shuffle(paths)


if __name__ == '__main__':
    main()
