from bs4 import BeautifulSoup
import requests as req
import lxml
from urllib.request import Request, urlopen
from multiprocessing import Pool

from parsing import get_page_doc, get_pages_links_stihiya
import sys
sys.setrecursionlimit(100000)

page_url = 'https://shop.wakepark.by/snowboarding/snowboards/'
pages_links = get_pages_links_stihiya(page_url)
# pages_links = list(dict.fromkeys(pages_links))


containers = list()

for link in pages_links:
    page_doc = get_page_doc(link)
    containers += page_doc.find_all("div", class_="border-0 rounded-0 h-100 product-card")


print(len(containers))

def start_parsing(container):
    link = container.find('a').get('href')
    title = container.find('img').get('alt').strip()

    print(title, link)


with Pool(10) as p:
    p.map(start_parsing, containers)