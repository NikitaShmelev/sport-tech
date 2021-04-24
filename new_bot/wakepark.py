import os
import lxml
import sys

from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
from multiprocessing import Pool

sys.setrecursionlimit(100000)


class Wakepark():

    def __init__(self):
        self.main_url = 'https://shop.wakepark.by/'
        self.skip_list = [
            'Бренды', 'Акции', 'Подарочные сертификаты', 'О нас',
            'Реквизиты', 'Преимущества', 'Таблица размеров', 'Обратная связь',
            'Контакты', 'Регистрация', 'Авторизация', 'Показать все', 'Доставка и оплата'
            ]

    def get_page_doc(self, url=None):
        page_url = self.main_url if not url else url
        hdr = {'User-Agent': 'Mozilla/5.0'}
        request = Request(page_url, headers=hdr)
        page = urlopen(request)
        soup = BeautifulSoup(page, 'lxml')
        return soup


    def get_categories(self, page_doc):
        result = dict()
        categories = page_doc.find_all("a", class_="nav-link dropdown-toggle text-uppercase font-weight-bold")
        del categories[-1]
        categories.append(page_doc.find("a", class_='nav-link text-uppercase font-weight-bold px-1'))
        with Pool(5) as p:
            sub_result = p.map(self.get_categories_with_pool, (categories))
        result = dict()
        for i in sub_result:
            result[i[0]] = i[1]
        return result


    def get_categories_with_pool(self, i):
        category_name = i.text.strip()
        if category_name not in self.skip_list:
            url = i.get('href')                
            doc = self.get_page_doc(url)
            sub_result = doc.find_all('a', class_='btn btn-light bg-white rounded-0 text-uppercase font-weight-bold px-3 py-2 mx-2 mb-3')
            links_to_subcategories = [i.get('href') for i in sub_result]
            titles = [i.text.strip() for i in sub_result]
            return (category_name, dict(zip(titles, links_to_subcategories)))