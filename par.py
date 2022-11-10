import requests
from bs4 import BeautifulSoup
import undetected_chromedriver
from PIL import Image
import time

from connection import cur, conn
from connection_bot import bot


def parser(url):
    """Функция открытия страницы с помощью Selenium"""

    options = undetected_chromedriver.ChromeOptions()
    options.add_argument("--headless")
    # скрытие окна
    driver = undetected_chromedriver.Chrome(
        executable_path="config/chromedriver",
        options=options
    )

    try:
        # получаем html страницу
        driver.get(url)
        time.sleep(8)
        html = driver.page_source
        soup = BeautifulSoup(html, "lxml")
        return soup

    except Exception as ex:
        print(ex)
    finally:
        driver.close()
        driver.quit()


def price_bs4(html, key, key_class):
    try:
        # находим(с помощью заданных данных в бд) и возвращаем цену
        all_product = html.find(key_class, class_=key).get_text()
        prise = int("".join([i for i in all_product.split() if i.isdigit()]))
        return prise
    except Exception as error:
        print(error)
        return 0


def download_image(page, id_product, key, name_key):
    try:
        # находим по заданным данным ссылку на фото
        image = page.find(key, class_=name_key)['src']

        p = requests.get(f"https:{image}")
        with open(f"images/{id_product}_avg.jpg", "wb") as f:
            f.write(p.content)
        # сохраняем фотографию с разными разрешениями
        img = Image.open(f"images/{id_product}_avg.jpg")
        img.thumbnail(size=(100, 100))
        img.save(f"images/{id_product}_min.jpg")

        img = Image.open(f"images/{id_product}_avg.jpg")
        img.thumbnail(size=(300, 300))
        img.save(f"images/{id_product}_avg.jpg")
        return 1

    except Exception as ex:
        print(ex)


def send_message(product, price):
    with open('config/profile.txt', 'rt', encoding='UTF-8') as file:
        id_user = file.readline()
    if id_user.isdigit():
        try:
            bot.send_message(int(id_user), f"""Цена на {product[2]} изменилась с {product[4]} на {price}
Успей купить!
{product[3]}""")
        except Exception as ex:
            print("Не удалось отправить сообщение пользователю...")
            print(ex)


def one_pars(product, work_bot=False):
    """ Функция парсинга для одного товара"""
    print(f"Парсинг товара с id{product[0]}")
    cur.execute("SELECT * FROM shops WHERE name = %s", (product[1],))
    keys = cur.fetchone()
    page = parser(product[3])
    # вызываем парсер страницы
    price = price_bs4(page, keys[2], keys[3])
    if product[4] > price > 0 and bot:
        send_message(product, price)
    # поиск цены с помощью BeautifulSoup
    cur.execute(f'Update urls set last_prices = %s where id = %s', (price, product[0]))
    # сохраняем новое значение цены
    cur.execute(f'INSERT INTO prices (id_product, price) VALUES (%s, %s)', (product[0], price))
    # сохраняем значение цены для графика
    if not product[7] and keys[4]:
        # если есть данные по фотографии, и она еще не скачана
        statys = download_image(page, product[0], keys[4], keys[5])
        cur.execute(f'Update urls set image = %s where id = %s', (statys, product[0]))


def all_pars(work_bot=False):
    """Функция парсинга всех товаров"""

    cur.execute("SELECT * FROM urls ORDER BY id")
    products = cur.fetchall()
    print("Начался парсинг...")
    for product in products:
        one_pars(product, work_bot=True)

    print("Парсинг успешно закончен")


def parsing_with_bot():
    all_pars(work_bot=True)


if __name__ == '__main__':
    all_pars()
    conn.close()
