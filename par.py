import time

import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import undetected_chromedriver
from multiprocessing.dummy import Pool as ThreadPool
import datetime
from PIL import Image
from connection import cur, conn


def parser(url):
    # useragent = UserAgent()
    # options.add_argument(f"user-agent={useragent.random}")
    # options.add_argument("--proxy-server=178.72.89.107")
    # options.add_argument("--disable-blink-features=AutomationControlled")

    options = undetected_chromedriver.ChromeOptions()
    # options.add_argument("--headless")
    driver = undetected_chromedriver.Chrome(
        executable_path="config/chromedriver",
        options=options
    )

    try:
        driver.get(url)
        time.sleep(5)
        html = driver.page_source
        # with open('11.txt', "wt", encoding='UTF-8') as f:
        #     f.write(html)
        soup = BeautifulSoup(html, "lxml")
        return soup

    except Exception as ex:
        print(ex)
    finally:
        driver.close()
        driver.quit()


def wb(html, key, key_class):
    try:
        all_product = html.find(key_class, class_=key).get_text()
        prise = int("".join([i for i in all_product.split() if i.isdigit()]))
        return prise
    except Exception as error:
        print(error)


def download_image(page, id_product, key, name_key):
    try:
        image = page.find(key, class_=name_key)['src']

        p = requests.get(f"https:{image}")
        with open(f"images/{id_product}_avg.jpg", "wb") as f:
            f.write(p.content)

        img = Image.open(f"images/{id_product}_avg.jpg")
        img.thumbnail(size=(100, 100))
        img.save(f"images/{id_product}_min.jpg")

        img = Image.open(f"images/{id_product}_avg.jpg")
        img.thumbnail(size=(300, 300))
        img.save(f"images/{id_product}_avg.jpg")
        return 1

    except Exception as ex:
        print(ex)


def one_pars(product):
    cur.execute("SELECT * FROM shops WHERE name = %s", (product[1],))
    keys = cur.fetchone()
    page = parser(product[3])
    price = wb(page, keys[2], keys[3])
    cur.execute(f'Update urls set last_prices = %s where id = %s', (price, product[0]))
    if not product[7] and keys[4]:
        statys = download_image(page, product[0], keys[4], keys[5])
        cur.execute(f'Update urls set image = %s where id = %s', (statys, product[0]))


def all_pars():

    cur.execute("SELECT * FROM urls ORDER BY id")
    products = cur.fetchall()
    for product in products:
        one_pars(product)


if __name__ == '__main__':
    # az = parser('https://www.mvideo.ru/products/smartfon-apple-iphone-14-plus-512gb-blue-esim-30064929')
    # with open('mv.txt', 'wt', encoding='UTF-8') as f:
    #     f.write(az)
    all_pars()
    conn.close()




#     pool = ThreadPool(4)
#
#     # Open the URLs in their own threads
#     # and return the results
#     results = pool.map(one_pars, products)
#
#     # Close the pool and wait for the work to finish
#     pool.close()
#     pool.join()
#     # for product in products:
#     #     one_pars(product)