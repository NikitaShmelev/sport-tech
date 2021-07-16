from bs4 import BeautifulSoup
import lxml
from urllib.request import Request, urlopen

class Darsi():


    def __init__(self):
        self.main_url = 'https://darsi.by/'


    def get_page_doc(self, url=None):
        page_url = self.main_url if not url else url
        hdr = {'User-Agent': 'Mozilla/5.0'}
        request = Request(page_url, headers=hdr)
        page = urlopen(request)
        soup = BeautifulSoup(page, 'lxml')
        return soup


    def get_categories(self, page_doc):
        result = dict()
        links_containers = page_doc.find('div', class_='t-menusub').find_all('a', class_='t-menusub__link-item t-name t-name_xs')
        for item in links_containers:
            result[item.text.strip()] = item['href'] if 'http' in item['href'] else 'https://darsi.by' + item['href']
            print(item.text.strip(), result[item.text.strip()])
        return result


    def parse_category(self, url, category):
        print(url, category)
        