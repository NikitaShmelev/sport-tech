from bs4 import BeautifulSoup
import requests as req
import lxml
from urllib.request import Request, urlopen
# from multiprocessing import Pool
import sys
import os
import time
# from dominant import *
# from rollershop import get_page_doc_rollershop
from wakepark import wakepark_categories, get_pages_links_wakepark, parse_category_wakepark

sys.setrecursionlimit(100000)


def get_page_doc(page_url):
    hdr = {'User-Agent': 'Mozilla/5.0'}
    request = Request(page_url, headers=hdr)
    page = urlopen(request)
    soup = BeautifulSoup(page, 'lxml')
    # os.system('clear')
    return soup

def make_folders(result, shop):
    for key in result.keys():
        try:
            os.mkdir(f'./{shop}/{key}')
        except:
            pass
        for sub_key in result[key]:
            try:
                os.mkdir(f'./{shop}/{key}/{sub_key}')
            except:
                pass



def get_categories(page_doc, shop, result=dict()):
    if shop == 'FAMILY BOARDSHOP':
        result = wakepark_categories(page_doc)    
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
    elif shop == 'Dominant':
        categories = [i.text.strip() for i in page_doc.find_all('span', class_='name option-font-bold')]
        categories = categories[0:round(len(categories)/2)]
        sub_categories = page_doc.find_all('div', class_='burger-dropdown-menu toggle_menu')
        for item in enumerate(sub_categories):
            sub_result = item[1].find_all('a')
            links = ['https://dominant.by' + i.get('href') for i in sub_result]
            titles = [i.get('title') for i in sub_result]
            result[categories[item[0]]] = dict(zip(titles, links))
        result['Балансборды'] = 'https://dominant.by/catalog/balansbordy/'
        result['Распродажи'] = 'https://dominant.by/catalog/sale/'
    make_folders(result, shop)
    return result


def get_page_doc_rollershop(url):
    hdr = {'User-Agent': 'Mozilla/5.0'}
    request = req.get(url, headers=hdr)
    request.encoding
    soup = BeautifulSoup(request.content.decode('utf-8', 'ignore'), 'lxml')
    # try:
    #     os.system('clear')
    # except:
    #     os.system('cls')
    return soup


def get_products_links_pollershop(url):
    page_doc = get_page_doc_rollershop(url)
    containers = page_doc.find_all('div', class_='item product-layout')
    result = [i.find('div', class_='name').find('a').get('href') for i in containers]
    return result





def get_pages_links_dominant(url):
    page_doc = get_page_doc(url)
    result = [i.get('href') for i in page_doc.find('div', class_='nums').find_all('a')]
    return result







def parse_category(shop, url, result = list()):

    if shop == 'FAMILY BOARDSHOP':
        result = parse_category_wakepark(url)

    elif shop == 'Rollershop':
        pages_links = get_products_links_pollershop(url)
        for link in enumerate(pages_links):
            page_doc = get_page_doc_rollershop(link[1])
            title = page_doc.find('h1', itemprop='name').text.strip()
            price = float(page_doc.find('span', itemprop='price').text.strip().replace(' руб.', ''))
            sizes = [i.text.strip() for i in page_doc.find_all('option')]
            if sizes:
                result.append([title, price, sizes, link[1]])
            else:
                result.append([title, price, link[1]])
            try:
                os.system('clear')
            except:
                os.system('cls')
            print(f'{link[0]*100/len(pages_links)}%')

    elif shop == 'Dominant':
        pages_links = [url]
        page_doc = get_page_doc(url)
        div = page_doc.find('div', class_='module-pagination')
        if div:
            first_page_number = int(div.find_all('a', class_='dark_link')[0].text.strip())
            last_page_number = int(div.find_all('a', class_='dark_link')[-1].text.strip())
            for number in range(first_page_number, last_page_number+1):
                pages_links.append(f'{url}?PAGEN_1={number}')
        all_links = []
        for link in enumerate(pages_links):
            # time.sleep()
            page_doc = get_page_doc(link[1])
            item_links = ['https://dominant.by' + i.get('href') for i in page_doc.find_all('a', class_='dark_link option-font-bold font_sm')]
            all_links += item_links
        for url in enumerate(all_links):
            page_doc = get_page_doc(url[1])
            title = page_doc.find('h1', id='pagetitle').text.strip()
            current_price = page_doc.find('div', class_='price font-bold font_mxs').text.strip().replace(
                                                                                                'от ','').replace(
                                                                                                        ' руб.', '').replace(
                                                                                                                    ' /шт', '').replace('\'','')
            if len(current_price) > 6:
                current_price = current_price[0] + current_price[2:]
            else:
                current_price = current_price
            old_price = 'пока не добывается :('#page_doc.find('div', class_='sale-number rounded2')#.text.strip()

            try:
                sizes = [i.text.strip() for i in page_doc.find('div', class_='bx_size').find_all('span', class_='cnt')]
            except:
                sizes = (None, )
            try:
                os.system('clear')
            except:
                os.system('cls')
            print(f'{url[0]*100/len(all_links)}%')
            if [title, current_price, sizes] not in result:
                result.append([title, current_price, old_price, sizes, url[1]])
            else:
                break
    return result