from bs4 import BeautifulSoup
import requests as req

import lxml

from funcs import get_page_doc
from openpyxl import Workbook, load_workbook


from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

class FamilyBoardshop():


    def __init__(self):
        self.main_url = 'https://shop.wakepark.by/'
        self.categories = self.__get_categories__()


    def __get_categories__(self):
        page_doc = get_page_doc(self.main_url)
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


    def get_exel(self, categories):
        # проверка ссылок на нормальность
        # driver = webdriver.Chrome(ChromeDriverManager().install())
        # driver.get("http://www.google.com")
        # driver.close()
        

        for key in categories.keys():
            print(categories[key])
            self.parse_category(categories[key])
            # print(page_doc)
            break
            # driver.get(categories[key])
        return True
    
    def __get_pages_links__(self, url):
        page_doc = get_page_doc(url)
        pages_links = [
            i.find_all('a') for i in page_doc.find_all("ul", class_="pagination")
            ]
        result = list()
        for i in pages_links:
            for j in i:
                result.append(j.get('href'))
        # result = [
        #     i.get('href') for i in pages_links
        # ]
        
        return result
    
    def parse_category(self, url):
        pages_links = self.__get_pages_links__(url)
        containers = list()
        for link in pages_links:
            page_doc = get_page_doc(link)
            containers += page_doc.find_all("div", class_="border-0 rounded-0 h-100 product-card")
            break
        for container in containers:
            # get title 
            link = container.find('a').get('href')
            title = container.find('img').get('alt').strip()
            # price = container.find_all('span')
            price = None
            
            # print(type(container))
            if price:
                print(title, link, price)
            else:
                doc = get_page_doc(link)
                prices = doc.find('div', class_='p-price h2').text.strip()
                prices = prices.split(' ')
                result = []
                for item in prices:
                    try:
                        if int(item[0]):
                            result.append(item)
                    except ValueError :
                        for letter in enumerate(item):
                            if letter[1] in ['1', '2', '3', '4', '5', '6', '7', '8', '9']:
                                result.append(item[letter[0]:-1])
                                break
                    
            print(title, link, result)
            # break

class Stihiya:

    def __init__(self):
        self.longboards_url = 'https://www.stihiya-shop.by/catalog/skateboards_and_longboards/longboards/'
        self.roller_skates = dict()
        self.longboards = dict()

    def __get_titles_and_prices__(self, page_doc):
        titles = [
                i.text.strip() for i in page_doc.find_all(
                        "h6", class_="product-cat-title")
                ]
        prices = [
                i.text.strip() for i in page_doc.find_all(
                    'div', class_='product-cat-price-current'
                )
            ]
        return dict(zip(titles, prices))

    def get_longboards(self):
        page_doc = get_page_doc(self.longboards_url)
        longboards = self.__get_titles_and_prices__(page_doc)
        # links = self.__get_links_from_page__(page_doc)
        return longboards


class Dominant():

    def __init__(self):
        self.longboards_url = 'https://dominant.by/catalog/longboardandcruiser/longbordy-i-kruizery-v-sbore/'
        self.roller_skates = dict()
        self.longboards = dict()
        