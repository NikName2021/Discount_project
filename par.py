import time

import requests
from bs4 import BeautifulSoup
from seleniumwire import webdriver
from fake_useragent import UserAgent
import undetected_chromedriver


url = 'https://www.wildberries.ru/catalog/64179466/detail.aspx?targetUrl=SG'
url_ozon = 'https://www.ozon.ru/product/obuchayushchie-igry-bondibon-schitay-i-proveryay-robot-295141390/?sh=YaM6IJk57A'
market = "https://market.yandex.ru/product--igrovoi-nabor-hasbro-spidey-and-his-amazing-friends-spaidi-i-transport-f1940/976314346?cpc=sBvQwFKiyQZq7wEprcgHPzqHSPaR2BgtsUZkeoGmBMxjjYY3CUK4-Twi91yrL0s9A0QxQSpKfhcEPHxEK7QQlog1ybhCOn5t0lX3xTF4iTkK2wAVkdDIpAkvGuUdG6Jzu-gqFBXcoBw1uWCWef1J16G9qNSmV5OQp1TyDZWARMiAyEWqbbPrAdy12vslZagq3fwpErwEIOw%2C&from-show-uid=16654909365785718463400002&sku=976314346&do-waremd5=AyUsfy2hFJCfoPgTWaqcKA&sponsored=1&cpa=1"
ali = "https://aliexpress.ru/item/1005003818004054.html?pdp_ext_f=%7B%22ship_from%22%3A%22RU%22%2C%22sku_id%22%3A%2212000027263069516%22%7D&pdp_npi=2%40dis%21RUB%2169%C2%A0990%2C00%20руб.%2166%C2%A0490%2C50%20руб.%21%21%21%21%21%40211675cd16655186220706200e687e%2112000027263069516%21gdf&pvid=29d27cb7-8a50-427e-a92c-5850425ac012&scm=1007.31960.273946.0&scm-url=1007.31960.273946.0&scm_id=1007.31960.273946.0&sku_id=12000027263069516&spm=a2g2w.home.0.1.75df501di0A5nh&utparam=%257B%2522process_id%2522%253A%25221001%2522%252C%2522x_object_type%2522%253A%2522product%2522%252C%2522pvid%2522%253A%252229d27cb7-8a50-427e-a92c-5850425ac012%2522%252C%2522belongs%2522%253A%255B%257B%2522id%2522%253A%2522477005%2522%252C%2522type%2522%253A%2522dataset%2522%257D%255D%252C%2522pageSize%2522%253A%252220%2522%252C%2522language%2522%253A%2522ru%2522%252C%2522scm%2522%253A%25221007.31960.273946.0%2522%252C%2522countryId%2522%253A%2522RU%2522%252C%2522tpp_buckets%2522%253A%252221669%25230%2523265320%252345_21669%25234190%252319165%2523764_21960%25230%2523273946%25230%2522%252C%2522x_object_id%2522%253A%25221005003818004054%2522%257D"
all_in = "https://www.vseinstrumenti.ru/instrument/shlifmashiny/bolgarka-ushm/sturm/ag9012te/"
mvideo = "https://www.mvideo.ru/products/smartfon-realme-c35-4--64gb-glowing-black-rmx3511-30063299"
mega = "https://sbermegamarket.ru/catalog/details/utyug-endever-delta-103-600000756981/"


def wildberries():
    useragent = UserAgent()

    options = undetected_chromedriver.ChromeOptions()

    # options.add_argument(f"user-agent={useragent.random}")
    # options.add_argument("--proxy-server=178.72.89.107")
    # options.add_argument("--disable-blink-features=AutomationControlled")

    # options.add_argument("--headless")

    driver = undetected_chromedriver.Chrome(
        executable_path="C:/python/mainproject/config/chromedriver",
        options=options
    )

    try:
        driver.get(mega)
        time.sleep(5)
        html = driver.page_source
        with open("ozon.txt", "w", encoding='utf-8') as f:
            f.write(html)
        # soup = BeautifulSoup(html, "lxml")
        # all_product = soup.find("ins", class_="price-block__final-price")
        # print(all_product.text.split())
    except Exception as ex:
        print(ex)
    finally:
        driver.close()
        driver.quit()


def ozon():
    main = requests.get("https://www.ozon.ru/api/composer-api.bx/page/json/v2?url=%2Fproduct%2Fnavolochka-dekorativnaya-le-gobelin-novogodniy-vecher-bezhevyy-fon-45h45-sm-333913955%2F%3Flayout_container%3DpdpMobileThemePage2%26layout_page_index%3D3%26sh%3DYaM6INHCfA")
    print(main.text)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':

    wildberries()









# with open("main.json", "w") as file:
#     json.dump(soup, file, indent=4, ensure_ascii=False)
# all_product = soup.find_all(ins, class="price-block__final-price")
# print(all_product)