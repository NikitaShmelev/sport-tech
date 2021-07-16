from bs4 import BeautifulSoup
import lxml
from urllib.request import Request, urlopen
import requests as req
import os


class Rollershop():
    
    
    def __init__(self):
        self.main_url = 'https://rollershop.by/'

    
    def get_page_doc(self, url=None):
        page_url = self.main_url if not url else url
        hdr = {'User-Agent': 'Mozilla/5.0'}
        request = req.get(page_url, headers=hdr)
        request.encoding
        soup = BeautifulSoup(request.content.decode('utf-8', 'ignore'), 'lxml')
        return soup

    
    def get_categories(self, page_doc):
        result = dict()
        categories = page_doc.find_all('li', class_='top has_sub top')
        for item in categories:
            title = item.find('a', class_='sub_trigger').text.strip()
            sub_titles = [i.text.strip() for i in item.find_all('a', class_='main-menu')]
            sub_links = [i.get('href') for i in item.find_all('a', class_='main-menu')]
            result[title] = dict(zip(sub_titles, sub_links))
        return result

    def __get_products_links_pollershop__(self, url):
        page_doc = self.get_page_doc(url)
        containers = page_doc.find_all('div', class_='item product-layout')
        result = [i.find('div', class_='name').find('a').get('href') for i in containers]
        return result


    def parse_category(self, url, category):
        result = list()
        pages_links = self.__get_products_links_pollershop__(url)
        for link in enumerate(pages_links):
            if len(link) > 1:
                page_doc = self.get_page_doc(link[1])
            else:
                page_doc = self.get_page_doc(link)
            title = page_doc.find('h1', itemprop='name').text.strip()
            current_price = float(page_doc.find('span', itemprop='price').text.strip().replace(' руб.', ''))
            try:
                old_price = float(
                    page_doc.find('div', class_='price-old').find('span', class_='amount').text.strip().replace(' руб.', '')
                    )
            except:
                old_price = None
            # print(current_price, old_price)
            sizes = [i.text.strip() for i in page_doc.find_all('option')][1:]
            # print(title, [current_price, old_price], sizes, link[1])
            dict_for_return = {
                'category': category,
                'title': title,
                'current_price': current_price,
                'old_price': old_price,
                'sizes': sizes,
                'url' :link[1],
                'other_values': list(),
            }
            result.append(dict_for_return)
        return result
        