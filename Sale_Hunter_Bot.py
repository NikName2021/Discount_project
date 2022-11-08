import telebot
from connection_bot import bot


@bot.message_handler(commands=['start'])
def start_message(message):
    id_user = 1232435163
    bot.send_message(id_user, 'Привет, ты написал мне /start')

