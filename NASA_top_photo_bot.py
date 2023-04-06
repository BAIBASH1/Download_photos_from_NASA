import telegram
import os
import argparse
import time
import random
from pytimeparse import parse
from dotenv import load_dotenv


load_dotenv()
TG_TOKEN = os.environ['TG_TOKEN']


def main():
    parser = argparse.ArgumentParser(
        description='Бот присылает фотографии из указанной директории,'
                    ' с указанным периодом (дефолтно период равен 4ем часам),'
                    ' если фотографии закончатся,'
                    ' начнет случайном порядке присылась фотографии'
    )
    parser.add_argument(
        '--directory',
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
    bot = telegram.Bot(token=TG_TOKEN)
    paths = []
    for entry in os.scandir(args.directory):
        paths.append(entry.path)
    period = parse(args.period)
    while True:
        for path in paths:
            bot.send_document(
                chat_id='@nasa_pictires',
                document=open(path, 'rb')
            )
            time.sleep(period)
        random.shuffle(paths)


if __name__ == '__main__':
    main()
