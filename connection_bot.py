import os
import telebot
from dotenv import load_dotenv

load_dotenv()

try:
    BOT_TOKEN = os.getenv("BOT_TOKEN")
    bot = telebot.TeleBot(BOT_TOKEN)

except Exception as ex:
    print(ex)
