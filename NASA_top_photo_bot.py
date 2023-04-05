import telegram
from dotenv import load_dotenv
import os

load_dotenv()
TG_TOKEN = os.environ['TG_TOKEN']
bot = telegram.Bot(token=TG_TOKEN)
bot.send_message(chat_id='@nasa_pictires', text='Тестовое сообщение' )

