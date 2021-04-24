from bs4 import BeautifulSoup
import lxml
from urllib.request import Request, urlopen
import os

class Dominant():
    
    
    def __init__(self):
        self.main_url = 'https://dominant.by/'


    def get_page_doc(self, url=None):
        page_url = self.main_url if not url else url
        hdr = {'User-Agent': 'Mozilla/5.0'}
        request = Request(page_url, headers=hdr)
        page = urlopen(request)
        soup = BeautifulSoup(page, 'lxml')
        return soup
        

    def get_categories(self, page_doc):
        result = dict()
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
        return result