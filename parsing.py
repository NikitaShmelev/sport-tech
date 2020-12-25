from bs4 import BeautifulSoup
import requests as req
import lxml
from urllib.request import Request, urlopen
from multiprocessing import Pool
import sys
sys.setrecursionlimit(100000)

def get_page_doc(page_url):
    hdr = {'User-Agent': 'Mozilla/5.0'}
    
    request = Request(page_url, headers=hdr)
    page = urlopen(request)
    soup = BeautifulSoup(page, 'lxml')
    return soup

def get_categories(page_doc, shop):
    result = dict()
    if shop == 'FAMILY BOARDSHOP':
        categories = page_doc.find_all("a", class_="nav-link dropdown-toggle text-uppercase font-weight-bold")
        del categories[-1]
        categories.append(page_doc.find("a", class_='nav-link text-uppercase font-weight-bold px-1'))
        for i in categories:
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
                result[category_name] = dict(zip(titles, links_to_subcategories))
            
    elif shop == 'Rollershop':
        # require te get again soup becouse some faggot created this site
        page_doc = get_page_doc_rollershop('https://rollershop.by/')
        categories = page_doc.find_all('li', class_='top has_sub top')
        # <li class="top"><a href="https://rollershop.by/samokaty" class="">Самокаты</a></li>
        # some dolbaeb did it 
        # get link via your hands
        for item in categories:
            title = item.find('a', class_='sub_trigger').text.strip()
            sub_titles = [i.text.strip() for i in item.find_all('a', class_='main-menu')]
            sub_links = [i.get('href') for i in item.find_all('a', class_='main-menu')]
            result[title] = dict(zip(sub_titles, sub_links))
    return result


def get_page_doc_rollershop(url):
    hdr = {'User-Agent': 'Mozilla/5.0'}
    request = req.get(url, headers=hdr)
    request.encoding
    soup = BeautifulSoup(request.content.decode('utf-8', 'ignore'), 'lxml')
    return soup


def get_products_links_pollershop(url):
    page_doc = get_page_doc_rollershop(url)
    containers = page_doc.find_all('div', class_='item product-layout')
    result = [i.find('div', class_='name').find('a').get('href') for i in containers]
    return result


def parse_category_rollershop(url):
    pages_links = get_products_links_pollershop(url)
    resut = list()
    for link in pages_links:
        page_doc = get_page_doc_rollershop(link)
        title = page_doc.find('h1', itemprop='name').text.strip()
        price = float(page_doc.find('span', itemprop='price').text.strip().replace(' руб.', ''))
        sizes = [i.text.strip() for i in page_doc.find_all('option')]
        if sizes:
            resut.append([title, price, sizes, url])
        else:
            resut.append([title, price, url])
        print(title, price, sizes, link)
    return resut


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

def parse_category_wakepark(url):
    result = list()
    pages_links = get_pages_links_wakepark(url)
    containers = list()
    for link in pages_links:
        page_doc = get_page_doc(link)
        containers += page_doc.find_all("div", class_="border-0 rounded-0 h-100 product-card")
        # break
    for container in containers:
        link = container.find('a').get('href')
        title = container.find('img').get('alt').strip()
        if title == 'Скидочная карта SHOP.WAKEPARK.BY':
            continue
        try:
            doc = get_page_doc(link)
        except:
            continue
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
        result.append([title, [float(i[0:-1]) for i in prices], link])
        print(title, prices, link)
    return result