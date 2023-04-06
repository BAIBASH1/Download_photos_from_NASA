import telegram
from dotenv import load_dotenv
import os
import argparse
import time
import random
from pytimeparse import parse

load_dotenv()
TG_TOKEN = os.environ['TG_TOKEN']

parser = argparse.ArgumentParser(description='')
parser.add_argument('--directory', help='Укажите путь к папке из которой необходимо присылать фотографии')
parser.add_argument('--period', default='4h', help='Укажите период между отправками сообщений, в формате число + текст, например: 12s (равно 12 сек); 1.2h2m1c (равно 1.2*60*60+2*60+1=4441 сек); 1day (равно 86400)')
args = parser.parse_args()
bot = telegram.Bot(token=TG_TOKEN)
paths = []
for entry in os.scandir(args.directory):
    paths.append(entry.path)
period = parse(args.period)
# bot.send_message(chat_id='@nasa_pictires', text='Тестовое сообщение')

while True:
    for path in paths:
        bot.send_document(chat_id='@nasa_pictires', document=open(path, 'rb'))
        time.sleep(period)
    random.shuffle(paths)

