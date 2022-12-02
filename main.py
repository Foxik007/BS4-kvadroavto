import csv
import json
import os
from time import sleep
from bs4 import BeautifulSoup
import requests
import lxml
from datetime import datetime

def get_all_pages():
    r = requests.get(url='https://www.kvadroavto.ru/catalog/sport_i_otdykh/mobilnyy_elektrotransport/')
    if not os.path.exists('data'):
        os.mkdir('data')
    with open('data/page_1.html','w',encoding='utf8') as f:
        f.write(r.text)


    with open('data/page_1.html',encoding='utf8') as f:
        src = f.read()

    soup = BeautifulSoup(src,'lxml')
    pages_count = int(soup.find('div',class_='module-pagination').find_all('a')[-1].text)

    for i in range(1,pages_count + 1):
        url = f'https://www.kvadroavto.ru/catalog/sport_i_otdykh/mobilnyy_elektrotransport/?PAGEN_1={i}'

        r = requests.get(url)

        with open(f'data/page_{i}.html','w',encoding='utf8') as f:
            f.write(r.text)

        sleep(1)

    return pages_count + 1


def collect_data(pages_count):
    cur_date = datetime.now().strftime('%d_%m_%Y')

    with open(f'data_{cur_date}.csv','w',encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(
            (
                'Название',
                'Ссылка',
                'Изображение'
            )

        )

    data = []
    for page in range(1,pages_count):
        with open(f'data/page_{page}.html',encoding='utf-8') as f:
            src = f.read()

        soup = BeautifulSoup(src,'lxml')
        item_cards = soup.find_all('div',class_="item_block col-4 col-md-3 col-sm-6 col-xs-6")

        for item in item_cards:
            product_article = item.find('div',class_="item-title").text.strip()
            product_url = 'https://www.kvadroavto.ru/' + item.find('a').get('href')
            product_image = 'https://www.kvadroavto.ru/' + item.find('img').get('src')
            data.append(
                {
                    'product_article':product_article,
                    'product_url':product_url,
                    'product_image': product_image
                }
            )
            with open(f'data_{cur_date}.csv', 'a',encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(
                    (
                        product_article,
                        product_url,
                        product_image
                    )

                )
        print(f'[INFO] - Обработана страница {page}/6')

    with open(f'scooter_{cur_date}.json', 'a',encoding='utf-8') as f:
        json.dump(data,f,indent=4,ensure_ascii=False)


def main():
    pages_count = get_all_pages()
    collect_data(pages_count=pages_count)


if __name__ == '__main__':
    main()