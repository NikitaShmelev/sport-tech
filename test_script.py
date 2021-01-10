from bs4 import BeautifulSoup
import requests as req
import lxml
from urllib.request import Request, urlopen
from multiprocessing import Pool

# from parsing import get_page_doc, get_pages_links_stihiya
import sys
sys.setrecursionlimit(100000)



url = 'https://dominant.by/catalog/clothes/'

hdr = {'User-Agent': 'Mozilla/5.0'}
request = req.get(url, headers=hdr)
# request.encoding
soup = BeautifulSoup(request.content.decode('utf-8', 'ignore'), 'lxml')
div = soup.find('div', class_='module-pagination')
links = ['https://dominant.by' + i.get('href') for i in div.find_all('a', class_='dark_link')]
# corrent_count_of_links = links[-1][(links[-1].index('=') + 1):]
# print(corrent_count_of_links)

request = req.get(links[-2], headers=hdr)
new_doc = BeautifulSoup(request.content.decode('utf-8', 'ignore'), 'lxml')
div = soup.find('div', class_='module-pagination')
# links = ['https://dominant.by' + i.get('href') for i in div.find_all('a', class_='dark_link')]
print(div.find_all('a', class_='dark_link'))
first_page_number = div.find_all('a', class_='dark_link')[0].text.strip()
last_page_number = div.find_all('a', class_='dark_link')[-1].text.strip()#.replace('...', '')
print(first_page_number, last_page_number)















# page_url = 'https://shop.wakepark.by/snowboarding/snowboards/'
# pages_links = get_pages_links_stihiya(page_url)
# # pages_links = list(dict.fromkeys(pages_links))


# containers = list()

# for link in pages_links:
#     page_doc = get_page_doc(link)
#     containers += page_doc.find_all("div", class_="border-0 rounded-0 h-100 product-card")


# print(len(containers))

# def start_parsing(container):
#     link = container.find('a').get('href')
#     title = container.find('img').get('alt').strip()

#     print(title, link)


# with Pool(10) as p:
#     p.map(start_parsing, containers)