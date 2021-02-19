from bs4 import BeautifulSoup
import requests as req
from multiprocessing import Pool
import lxml
from urllib.request import Request, urlopen
# from parsing import get_page_doc
import time

def get_page_doc(page_url):
    hdr = {'User-Agent': 'Mozilla/5.0'}
    request = Request(page_url, headers=hdr)
    page = urlopen(request)
    soup = BeautifulSoup(page, 'lxml')
    # os.system('clear')
    return soup

def get_pages_links_wakepark(url):
    page_doc = get_page_doc(url)
    pages_links = [
        i.find_all('a') for i in page_doc.find_all("ul", class_="pagination")
        ]
    result = list()
    result.append(url)
    for i in pages_links:
        for j in i:
            result.append(j.get('href'))
    result = list(dict.fromkeys(result))
    return result

def get_categories_pool(i):
    category_name = i.text.strip()
    skip_list = [
        'Бренды', 'Акции', 'Подарочные сертификаты', 'О нас',
        'Реквизиты', 'Преимущества', 'Таблица размеров', 'Обратная связь',
        'Контакты', 'Регистрация', 'Авторизация', 'Показать все', 'Доставка и оплата'
        ]
    if category_name not in skip_list:
        url = i.get('href')                
        doc = get_page_doc(url)
        sub_result = doc.find_all('a', class_='btn btn-light bg-white rounded-0 text-uppercase font-weight-bold px-3 py-2 mx-2 mb-3')
        """Searching for sub_cagories object in row above. Result contains tag <a>."""
        links_to_subcategories = [i.get('href') for i in sub_result]
        titles = [i.text.strip() for i in sub_result] # get titles of categories
        return (category_name, dict(zip(titles, links_to_subcategories)))


def wakepark_categories(page_doc):
    result = dict()
    categories = page_doc.find_all("a", class_="nav-link dropdown-toggle text-uppercase font-weight-bold")
    del categories[-1]
    categories.append(page_doc.find("a", class_='nav-link text-uppercase font-weight-bold px-1'))
    with Pool(10) as p:
        sub_result = p.map(get_categories_pool, (categories))
    result = dict()
    for i in sub_result:
        result[i[0]] = i[1]
    return result


def parse_containers(container):
    link = container.find('a').get('href')
    title = container.find('img').get('alt').strip()
    if title != 'Скидочная карта SHOP.WAKEPARK.BY':
        try:
            doc = get_page_doc(link)
        except:
            pass
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
        print(title, prices, link)
        return [title, [float(i[0:-1]) for i in prices], link]


def parse_category_wakepark(url):
    result = list()
    pages_links = get_pages_links_wakepark(url)
    containers = list()
    for link in pages_links:
        page_doc = get_page_doc(link)
        containers += page_doc.find_all("div", class_="border-0 rounded-0 h-100 product-card")
        with Pool(10) as p:
            result += p.map(parse_containers, (containers))
    print(len(result))
    time.sleep(1)
    return result