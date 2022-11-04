import time
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import undetected_chromedriver
from multiprocessing.dummy import Pool as ThreadPool
import datetime
from connection import cur, conn


def parser(url):
    useragent = UserAgent()

    # options.add_argument(f"user-agent={useragent.random}")
    # options.add_argument("--proxy-server=178.72.89.107")
    # options.add_argument("--disable-blink-features=AutomationControlled")

    options = undetected_chromedriver.ChromeOptions()
    # options.add_argument("--headless")
    driver = undetected_chromedriver.Chrome(
        executable_path="C:/python/mainproject/config/chromedriver",
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
    except BaseException as error:
        print(error)


def all_pars():

    cur.execute("SELECT * FROM urls")
    products = cur.fetchall()
    # pool = ThreadPool(4)
    #
    # results = pool.map(one_pars, products)
    # pool.close()
    # pool.join()
    # one_pars(products[0])
    for product in products:
        one_pars(product)


def one_pars(product):
    cur.execute("SELECT * FROM shops WHERE name = %s", (product[1],))
    keys = cur.fetchall()[0]
    print(keys)
    price = wb(parser(product[3]), keys[2], keys[3])
    cur.execute(f'Update urls set last_prices = %s where id = %s', (price, product[0]))


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