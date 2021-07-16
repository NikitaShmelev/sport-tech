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
        self.current_category = None

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


    def parse_category(self, url, category):
        result = list()
        pages_links = self.__get_pages_links__(url)
        containers = list()
        self.current_category = category
        for link in pages_links:
            page_doc = self.get_page_doc(link)
            containers += page_doc.find_all("div", class_="border-0 rounded-0 h-100 product-card")
            with Pool(5) as p:
                result += p.map(self.__parse_containers__, (containers))
            p.close()
            p.join()
        return result

    def __get_pages_links__(self, url):
        page_doc = self.get_page_doc(url)
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


    def __parse_containers__(self, container):
        link = container.find('a').get('href')
        title = container.find('img').get('alt').strip()
        if title != 'Скидочная карта SHOP.WAKEPARK.BY':
            try:
                doc = self.get_page_doc(link)
            except:
                pass
            try:
                prices = doc.find('div', class_='p-price h2').text.strip()
            except:
                return None
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
            dict_for_return = {
                'category': self.current_category,
                'title': title,
                'current_price': float(prices[0]),
                'old_price': float(prices[1]),
                'sizes': None,
                'url' :link,
                'other_values': list(),
            }
            return dict_for_return