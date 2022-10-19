from bs4 import BeautifulSoup
import undetected_chromedriver

import json
import time


def wildberries(url):

    options = undetected_chromedriver.ChromeOptions()
    # options.add_argument("--headless")

    driver = undetected_chromedriver.Chrome(
        executable_path="./config/chromedriver",
        options=options
    )

    try:
        driver.get(url)
        time.sleep(3)
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(5)
        html = driver.page_source
        with open("main.html", "w", encoding='utf-8') as f:
            f.write(html)

    except Exception as ex:
        print(ex)
    finally:
        driver.close()
        driver.quit()


def my_soup():
    save_product = {}
    with open("main.html", "r", encoding='utf-8') as f:
        file = f.read()
    soup = BeautifulSoup(file, "lxml")
    all_product = soup.find_all(class_="product-card j-card-item j-good-for-listing-event") + \
        soup.find_all(class_="product-card j-card-item")

    for t, i in enumerate(all_product):
        name = i.find('span', class_="goods-name").get_text()
        brand = i.find('strong', class_="brand-name").get_text()
        link = i.find("a", class_="j-card-link", href=True)['href']
        try:
            price = " ".join(i.find('span', class_="price").find('ins', class_="lower-price").get_text().split())
        except AttributeError:
            price = None

        save_product[t] = {
            "Бренд": brand,
            "Название": name,
            "Цена": price,
            "Ссылка": link
        }

    with open('data.json', 'w', encoding='utf8') as outfile:
        json.dump(save_product, outfile, indent=4, ensure_ascii=False)


if __name__ == '__main__':
    my_url = "https://www.wildberries.ru/catalog/elektronika/smartfony-i-telefony/vse-smartfony"
    wildberries(my_url)
    my_soup()
