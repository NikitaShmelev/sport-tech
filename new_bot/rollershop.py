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