import json
from bs4 import BeautifulSoup
from selenium import webdriver
import time

# headers = {
#     "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36",
#     'X-Requested-With': 'XMLHttpRequest'
# }

def get_page():
    url="https://www.dns-shop.ru/catalog/17a89aab16404e77/videokarty/?stock=1&action=vygodnyekomplekty0000-tovarysoskidkoj0000&p=1"
    options = webdriver.ChromeOptions()
    options.add_argument(f"user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:92.0) Gecko/20100101 Firefox/92.0")
    # отключение режима webdriver
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.headless = True

    try:
        driver = webdriver.Chrome(
            executable_path="C:\\Users\\Марсик\\PycharmProjects\\pythonProject\\parcer\\parcer6\\chromedriver.exe",
            # условный браузер которому будет отдават команды(абослютный путь к драйверу)
            options=options
        )
        url = "https://www.dns-shop.ru/catalog/17a89aab16404e77/videokarty/?stock=1&action=vygodnyekomplekty0000-tovarysoskidkoj0000&p=1"
        driver.get(url=url)
        time.sleep(5)
        src = driver.page_source
        soup = BeautifulSoup(src, "lxml")

        paginations = soup.find_all("li", class_="pagination-widget__page")

        paginations_count = len(paginations) - 4

        for pagin in range(1, paginations_count+1):
            url = f"https://www.dns-shop.ru/catalog/17a89aab16404e77/videokarty/?stock=1&action=vygodnyekomplekty0000-tovarysoskidkoj0000&p={pagin}"
            driver.get(url=url)
            time.sleep(5)

            with open(f"media/index_selenium({pagin}).html", "w", encoding="utf-8" )as file:
                file.write(driver.page_source)#page souce получение исходный код html страницы

            print(f"Записано {pagin}/{paginations_count}")

        return paginations_count
    except Exception as ex:
        print(ex)
    finally:
        driver.close()
        driver.quit()

def get_info(pagination):
    result_data = []
    for pagin in range(1, pagination+1):
        with open(f"media/index_selenium({pagin}).html", encoding="utf-8") as file:
            src = file.read()

        soup = BeautifulSoup(src, "lxml")

        product_card = soup.find_all("div", class_="catalog-product ui-button-widget")

        for info_product in product_card:
            product_name = info_product.find("span").text
            product_url = "https://www.dns-shop.ru" + info_product.find("a").get("href")
            product_price = info_product.find("div", class_="product-buy__price").text
            product_category = info_product.find("div", class_="vobler").text

            result_data.append(
                {
                    "name": product_name,
                    "category": product_category,
                    "link": product_url,
                    "price": product_price,
                }
            )
        print(f"Обработано {pagin}/{pagination}")

    with open("result_data(videocards).json", "w", encoding='utf-8') as file:
        json.dump(result_data, file, indent=4, ensure_ascii=False)

def main():
    pagination = get_page()
    get_info(pagination = pagination)
if __name__ == '__main__':
    main()
