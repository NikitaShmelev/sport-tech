from bs4 import BeautifulSoup
import requests as req
import lxml
from urllib.request import Request, urlopen
import os

def get_page_doc_rollershop(url):
    hdr = {'User-Agent': 'Mozilla/5.0'}
    request = req.get(url, headers=hdr)
    request.encoding
    soup = BeautifulSoup(request.content.decode('utf-8', 'ignore'), 'lxml')
    return soup


def rollershop_categories(page_doc, result=dict()):
    categories = page_doc.find_all('li', class_='top has_sub top')
    for item in categories:
        title = item.find('a', class_='sub_trigger').text.strip()
        sub_titles = [i.text.strip() for i in item.find_all('a', class_='main-menu')]
        sub_links = [i.get('href') for i in item.find_all('a', class_='main-menu')]
        result[title] = dict(zip(sub_titles, sub_links))
    return result


def get_products_links_pollershop(url):
    page_doc = get_page_doc_rollershop(url)
    containers = page_doc.find_all('div', class_='item product-layout')
    result = [i.find('div', class_='name').find('a').get('href') for i in containers]
    return result


def parse_category_rollershop(url, category):
    result = list()
    pages_links = get_products_links_pollershop(url)
    for link in enumerate(pages_links):
        if len(link) > 1:
            page_doc = get_page_doc_rollershop(link[1])
        else:
            page_doc = get_page_doc_rollershop(link)
        title = page_doc.find('h1', itemprop='name').text.strip()
        current_price = float(page_doc.find('span', itemprop='price').text.strip().replace(' руб.', ''))
        try:
            old_price = float(
                page_doc.find('div', class_='price-old').find('span', class_='amount').text.strip().replace(' руб.', '')
                )
        except:
            old_price = None
        # print(current_price, old_price)
        sizes = [i.text.strip() for i in page_doc.find_all('option')]
        if sizes:
            result.append([category, title, [current_price, old_price], sizes, link[1]])
        else:
            result.append([category, title, [current_price, old_price], link[1]])
        
    return result
