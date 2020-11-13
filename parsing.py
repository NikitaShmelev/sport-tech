from bs4 import BeautifulSoup
import requests as req
import lxml
from urllib.request import Request, urlopen


def get_page_doc(page_url):
    site = page_url
    hdr = {'User-Agent': 'Mozilla/5.0'}
    req = Request(site, headers=hdr)
    page = urlopen(req)
    soup = BeautifulSoup(page, 'lxml')
    return soup

def get_categories_stihiya(page_doc):
    result = dict()
    categories = page_doc.find_all("a", class_="dropdown-item")

    for i in categories:
        category_name = i.text.strip()
        skip_list = [
            'Бренды', 'Акции', 'Подарочные сертификаты', 'О нас',
            'Реквизиты', 'Преимущества', 'Таблица размеров', 'Обратная связь',
            'Контакты', 'Регистрация', 'Авторизация', 'Показать все', 'Доставка и оплата'
            ]
        
        if category_name not in skip_list:
            result[category_name] = i.get('href')
        result['Сноуборды'] = 'https://shop.wakepark.by/snowboarding/snowboards/'

    return result


def get_pages_links_stihiya(url):
    page_doc = get_page_doc(url)
    pages_links = [
        i.find_all('a') for i in page_doc.find_all("ul", class_="pagination")
        ]
    result = list()
    result.append(url)
    for i in pages_links:
        for j in i:
            result.append(j.get('href'))
    return result


def parse_category_stihiya(url):
    pages_links = get_pages_links_stihiya(url)
    containers = list()
    result = list()
    for link in pages_links:
        page_doc = get_page_doc(link)
        containers += page_doc.find_all("div", class_="border-0 rounded-0 h-100 product-card")
        # break
    for container in containers:
        link = container.find('a').get('href')
        title = container.find('img').get('alt').strip()
        if title == 'Скидочная карта SHOP.WAKEPARK.BY':
            continue
        doc = get_page_doc(link)
        prices = doc.find('div', class_='p-price h2').text.strip()
        prices = prices.split(' ')
        if len(prices) == 2:
            if 'BYN' not in prices[1]:
                prices[0] = prices[0].replace('BYN', '') + prices[1]
                del prices[1]
            else:
                prices[0] = prices[0].replace('BYN', '')
                del prices[1]
        elif len(prices) == 3:
            for i in prices:
                if '\xa0\xa0' in i:
                    prices[1] = prices[1].replace("\t", "").replace("\n", "").replace('\xa0\xa0','').replace('BYN','')
                    del prices[2]
                    break
            else:
                prices[0] += prices[1]
                del prices[1]
                del prices[1]
                
        elif len(prices) == 4:
            prices[1] = prices[1].replace("\t", "").replace("\n", "").replace('\xa0\xa0','').replace('BYN','') + prices[2]
            del prices[2]
            del prices[2]
        else:
            prices[0] += prices[1]
            prices[2] = prices[2].replace("\t", "").replace("\n", "").replace('\xa0\xa0','').replace('BYN','') + prices[3]
            del prices[1]
            del prices[3]
            del prices[2]
        result.append([title, prices, link])
    return result