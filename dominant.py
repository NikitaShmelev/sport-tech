from bs4 import BeautifulSoup
import requests as req
import lxml
from urllib.request import Request, urlopen
import os


def get_page_doc(page_url):
    hdr = {'User-Agent': 'Mozilla/5.0'}
    request = Request(page_url, headers=hdr)
    page = urlopen(request)
    soup = BeautifulSoup(page, 'lxml')
    return soup


def dominant_categories(page_doc, result=dict()):
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


def parse_category_dominant(url, result=list()):
    pages_links = [url]
    page_doc = get_page_doc(url)
    div = page_doc.find('div', class_='module-pagination')
    if div:
        first_page_number = int(div.find_all('a', class_='dark_link')[0].text.strip())
        last_page_number = int(div.find_all('a', class_='dark_link')[-1].text.strip())
        for number in range(first_page_number, last_page_number+1):
            pages_links.append(f'{url}?PAGEN_1={number}')
    all_links = []
    for link in enumerate(pages_links):
        # time.sleep()
        page_doc = get_page_doc(link[1])
        item_links = ['https://dominant.by' + i.get('href') for i in page_doc.find_all('a', class_='dark_link option-font-bold font_sm')]
        all_links += item_links
    for url in enumerate(all_links):
        page_doc = get_page_doc(url[1])
        title = page_doc.find('h1', id='pagetitle').text.strip()
        current_price = page_doc.find('div', class_='price font-bold font_mxs').text.strip().replace(
                                                                                            'от ','').replace(
                                                                                                    ' руб.', '').replace(
                                                                                                                ' /шт', '').replace('\'','')
        if len(current_price) > 6:
            current_price = current_price[0] + current_price[2:]
        else:
            current_price = current_price
        old_price = 'пока не добывается :('#page_doc.find('div', class_='sale-number rounded2')#.text.strip()

        try:
            sizes = [i.text.strip() for i in page_doc.find('div', class_='bx_size').find_all('span', class_='cnt')]
        except:
            sizes = (None, )
        try:
            os.system('clear')
        except:
            os.system('cls')
        print(f'{url[0]*100/len(all_links)}%')
        if [title, current_price, sizes] not in result:
            result.append([title, current_price, old_price, sizes, url[1]])
        else:
            break
    return result