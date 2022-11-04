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


def download_image(page, id_product):
    try:
        image = page.find('img', class_='photo-zoom__preview j-zoom-image hide')['src']
        p = requests.get(f"https:{image}")
        with open(f"images/{id_product}.jpg", "wb") as f:
            f.write(p.content)

        img = Image.open(f"images/{id_product}.jpg")
        img.thumbnail(size=(100, 100))
        img.save(f"images/{id_product}_min.jpg")
        return 1

    except Exception as ex:
        print(ex)


def one_pars(product):
    cur.execute("SELECT * FROM shops WHERE name = %s", (product[1],))
    keys = cur.fetchone()
    page = parser(product[3])
    price = wb(page, keys[2], keys[3])
    cur.execute(f'Update urls set last_prices = %s where id = %s', (price, product[0]))
    if not product[7]:
        statys = download_image(page, product[0])
        cur.execute(f'Update urls set image = %s where id = %s', (statys, product[0]))


def all_pars():

    cur.execute("SELECT * FROM urls")
    products = cur.fetchall()
    for product in products:
        one_pars(product)
        return


if __name__ == '__main__':
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