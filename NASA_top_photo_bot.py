import telegram
from dotenv import load_dotenv
import os

load_dotenv()
TG_TOKEN = os.environ['TG_TOKEN']
bot = telegram.Bot(token=TG_TOKEN)
bot.send_message(chat_id='@nasa_pictires', text='Тестовое сообщение')
bot.send_document(chat_id='@nasa_pictires', document=open('Photos_of_the_day\image_for_1997-11-17.jpg', 'rb'))

