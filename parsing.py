from bs4 import BeautifulSoup
import requests as req
import lxml
from urllib.request import Request, urlopen


def get_page_doc(page_url):
    hdr = {'User-Agent': 'Mozilla/5.0'}
    # proxies = {"http": "http://10.10.1.10:3128",
                # "https": "http://10.10.1.10:1080"}
    # req.get(page_url, headers=hdr, proxies=proxies)
    # print("FUCK")
    req = Request(page_url, headers=hdr)
    page = urlopen(req)
    soup = BeautifulSoup(page, 'lxml')
    return soup

def get_categories_stihiya(page_doc):
    result = dict()
    categories = page_doc.find_all("a", class_="nav-link dropdown-toggle text-uppercase font-weight-bold")
    del categories[-1]
    categories.append(page_doc.find("a", class_='nav-link text-uppercase font-weight-bold'))
    
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
        result.append([title, prices, link])
        print(title, prices, link)
    return result