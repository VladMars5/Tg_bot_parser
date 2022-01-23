import requests
from bs4 import BeautifulSoup
import json

headers={
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/\
        signed-exchange;v=b3;q=0.9",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36",
}

def get_page_time(url):
    s = requests.Session()
    response = s.get(url=url, headers=headers)

    with open("media(time)/index.html", "w", encoding='utf-8') as file:
        file.write(response.text)

    with open("media(time)/index.html", encoding='utf-8') as file:
           src = file.read()

    soup = BeautifulSoup(src,"lxml")
    pagination = soup.find_all("a", class_="pager-item pager-item--num")
    pagination_count = int(pagination[-1].text)

    for pagin in range(1, pagination_count + 1):

        s = requests.Session()
        response = s.get(url=f"https://www.alltime.ru/watch/man/filter/reference:sale/?PAGEN_1={pagin}", headers=headers)

        with open(f"media(time)/index({pagin}).html", "w", encoding='utf-8') as file:
            file.write(response.text)

        print(f"Загружено {pagin}/{pagination_count}")

    return pagination_count


def get_info_time(pagination):
    result_data = []
    for pagin in range(1, pagination + 1):
        with open(f"media(time)/index({pagin}).html", encoding='utf-8') as file:
            src = file.read()

        soup = BeautifulSoup(src, "lxml")

        all_products_hrefs = soup.find_all("div", class_="catalog-item catalog-item--col4")

        for item in all_products_hrefs:
            name = item.find("div", class_="catalog-item-name text-h5").text.strip()
            item_href = "https://www.alltime.ru" + item.find("a").get("href").strip()
            new_price = item.find("span", class_="catalog-item-price text-h5").text.strip()
            old_price = item.find("span", class_="catalog-item-price_old text-h5")
            discount = item.find("div", class_="catalog-item-labels").text.strip()
            if old_price == None:
                old_price = 'Скидка по договоренности'
                discount = 'Скидка в салоне'
            else:
                old_price = old_price.text.strip()

            result_data.append(
                {
                    "name": name,
                    "url": item_href,
                    "new_price": new_price,
                    "old_price": old_price,
                    "discount": discount
                }
            )
        print(f"Обработано {pagin}/{pagination}")

    with open("result_data(time).json", "w", encoding='utf-8') as file:
        json.dump(result_data, file, indent=4, ensure_ascii=False)

def main():
    pagination = get_page_time(url="https://www.alltime.ru/watch/man/filter/reference:sale/?PAGEN_1=2")
    get_info_time(pagination=pagination)
if __name__ == '__main__':
    main()