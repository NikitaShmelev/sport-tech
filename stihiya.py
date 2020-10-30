from bs4 import BeautifulSoup
import requests as req
import lxml

class Stihiya:

    def __init__(self):
        self.longboards_url = 'https://www.stihiya-shop.by/catalog/skateboards_and_longboards/longboards/'
        self.roller_skates = dict()
        self.longboards = dict()

    
    def __get_page_doc__(self, page_url):
        resp = req.get(page_url)
        soup = BeautifulSoup(resp.text, 'lxml')
        return soup


    def __get_links_from_page__(self, page_doc):
        return tuple(
                'https://www.stihiya-shop.by' + i.find('a').get('href') for i in page_doc.find_all(
                    "h6", class_="product-cat-title"
                    )
                )

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
        page_doc = self.__get_page_doc__(self.longboards_url)
        longboards = self.__get_titles_and_prices__(page_doc)
        # links = self.__get_links_from_page__(page_doc)
        return longboards