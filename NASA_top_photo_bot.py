import telegram
from dotenv import load_dotenv
import os
import argparse
import time

load_dotenv()
TG_TOKEN = os.environ['TG_TOKEN']

parser = argparse.ArgumentParser(description='')
parser.add_argument('--directory', help='Укажите путь к папке из которой необходимо присылать фотографии')
parser.add_argument('--period', help='Укажите период между отправками сообщений, в формате число + текст, например: 12s (равно 12 сек); 1.2h2m1c (равно 1.2*60*60+2*60+1=4441 сек); 1day (равно 86400)')

bot = telegram.Bot(token=TG_TOKEN)
bot.send_message(chat_id='@nasa_pictires', text='Тестовое сообщение')
bot.send_document(chat_id='@nasa_pictires', document=open('Photos_of_the_day\image_for_1997-11-17.jpg', 'rb'))

