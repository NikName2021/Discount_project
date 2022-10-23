import time
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import undetected_chromedriver
from multiprocessing.dummy import Pool as ThreadPool
import datetime
from connection import cur, con


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
    products = cur.execute("SELECT * FROM urls").fetchall()[:3]
    az = datetime.datetime.now()

    for product in products:
        one_pars(product)
    print(datetime.datetime.now() - az)


def one_pars(product):
    keys = cur.execute("SELECT * FROM shops WHERE name = ?", (product[1],)).fetchall()[0]
    price = wb(parser(product[3]), keys[2], keys[3])
    cur.execute(f'Update urls set last_price = ? where id = ?', (price, product[0]))
    con.commit()


if __name__ == '__main__':
    all_pars()




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