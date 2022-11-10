from telebot import types
import threading
import asyncio
import schedule as schedule

from par import parsing_with_bot
from connection_bot import bot


@bot.message_handler(commands=['start'])
def start_message(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("Получить мой id")
    markup.add(item1)
    bot.send_message(message.chat.id,
                     'Привет, воспользуйся кнопкой, чтобы получить свой id для приложения', reply_markup=markup)


@bot.message_handler(content_types=['text'])
def get_id(message):
    if message.text == "Получить мой id":
        bot.send_message(message.chat.id, text=f"""Вот твой id для приложения:
{message.from_user.id}
Введи его в поле и сохрани, чтобы получать уведомления о скидках""")


def scheduler():
    """
    Функция - таймер
    """
    schedule.every(60).minutes.do(parsing_with_bot)
    # каждые час запускаем функцию "all_pars"
    while True:
        schedule.run_pending()


class Mybot(threading.Thread):
    """ Класс потока для запуска парсинга"""
    def __init__(self):
        super().__init__()

    def run(self) -> None:
        while True:
            try:
                bot.polling(none_stop=True)

            except Exception as e:
                print(e)


class MyParser(threading.Thread):
    """ Класс потока для запуска парсинга"""
    def __init__(self):
        super().__init__()

    def run(self) -> None:
        # all_pars()
        asyncio.create_task(scheduler())


if __name__ == '__main__':
    downloader = Mybot()
    parser = MyParser()
    downloader.start()
    parser.start()
    downloader.join()
    parser.join()


