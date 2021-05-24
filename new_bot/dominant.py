from bs4 import BeautifulSoup
import lxml
from urllib.request import Request, urlopen
from multiprocessing import Pool

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

    def __parse_with_pool__(self, url):
    
        page_doc = self.get_page_doc(url)
        title = page_doc.find('h1', id='pagetitle').text.strip()
        current_price = page_doc.find('div', class_='price font-bold font_mxs').text.strip().replace(
                                                                                            'от ','').replace(
                                                                                                    ' руб.', '').replace(
                                                                                                                ' /шт', '').replace('\'','')
        if len(current_price) > 6:
            current_price = current_price[0] + current_price[2:]
        else:
            current_price = current_price
        old_price = ':('
        try:
            sizes = [i.text.strip() for i in page_doc.find('div', class_='bx_size').find_all('span', class_='cnt')]
        except:
            sizes = (None, )

        dict_for_return = {
            'category': self.category,
            'title': title,
            'current_price': current_price,
            'old_price': old_price,
            'sizes': sizes,
            'url' :url,
            'other_values': list(),
        }
        # print([self.category, title, current_price, old_price, sizes, url[1]])
        return dict_for_return
    


    def parse_category(self, url, category):
        self.category = category
        sub_result = list()
        pages_links = [url]
        page_doc = self.get_page_doc(url)
        div = page_doc.find('div', class_='module-pagination')
        if div:
            first_page_number = int(div.find_all('a', class_='dark_link')[0].text.strip())
            last_page_number = int(div.find_all('a', class_='dark_link')[-1].text.strip())
            for number in range(first_page_number, last_page_number+1):
                pages_links.append(f'{url}?PAGEN_1={number}')
        all_links = []
        for link in enumerate(pages_links):
            # time.sleep()
            page_doc = self.get_page_doc(link[1])
            item_links = ['https://dominant.by' + i.get('href') for i in page_doc.find_all('a', class_='dark_link option-font-bold font_sm')]
            all_links += item_links
        with Pool(5) as p:
            sub_result += p.map(self.__parse_with_pool__, (all_links))
        p.close()
        p.join()
        result = list()
        result = [item for item in sub_result if item not in result]
        return result