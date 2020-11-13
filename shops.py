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
            print(key, '\n\n')
            self.parse_category(categories[key])
            break
        return True
    
    def __get_pages_links__(self, url):
        page_doc = get_page_doc(url)
        pages_links = [
            i.find_all('a') for i in page_doc.find_all("ul", class_="pagination")
            ]
        result = list()
        result.append(url)
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
            # break
        for container in containers:
            link = container.find('a').get('href')
            title = container.find('img').get('alt').strip()
            
            doc = get_page_doc(link)
            prices = doc.find('div', class_='p-price h2').text.strip()
            prices = prices.split(' ')
            if len(prices) == 1:
                print(
                    '!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!'
                )
            elif len(prices) == 2:
                prices[0] = prices[0].replace('BYN', '') + prices[1]
                del prices[1]
            elif len(prices) == 3:
                prices[0] += 'BYN'
                prices[1] = prices[1].replace("\t", "").replace("\n", "").replace('\xa0\xa0','').replace('BYN','') + 'BYN'
                del prices[2]
            elif len(prices) == 4:                
                prices[0] += 'BYN'
                prices[1] = prices[1].replace("\t", "").replace("\n", "").replace('\xa0\xa0','').replace('BYN','') + prices[2] + 'BYN'
                del prices[2]
                del prices[2]
            else:
               
                prices[0] += prices[1]
                prices[2] = prices[2].replace("\t", "").replace("\n", "").replace('\xa0\xa0','').replace('BYN','') + prices[3] + 'BYN'
                del prices[1]
                del prices[3]
                del prices[2]
               
            print(f"\n\n{title=}\n{link=}\n{prices=}\n")
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
        