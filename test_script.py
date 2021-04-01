from bs4 import BeautifulSoup
import requests as req
import lxml
from urllib.request import Request, urlopen
from multiprocessing import Pool
import os
import xlsxwriter
from openpyxl import load_workbook
# from parsing import get_page_doc, get_pages_links_stihiya
import sys
sys.setrecursionlimit(100000)




def get_column_for_prices(path):
    wb = load_workbook(path)
    ws = wb.active

    for row in enumerate(ws.iter_rows()):
        if row[0] == 1:
            for cell in enumerate(row[1]):
                print(cell)
    #     sub_res = list()
    #     
    #         if cell.value == 'Category':
    #             break
    #         else:
    #             sub_res.append(cell.value)
    #     else:
    #         result[sub_res[0]] = dict(key=sub_res[1], value=sub_res[2:3])
    #         print(f'{result[sub_res[0]]}')
    # return result


if __name__ == '__main__':
    print(os.listdir())
    get_column_for_prices('./Rollershop/Роликовые коньки/Детские ролики/Детские ролики.xlsx')


# def get_page_doc(page_url):
#     hdr = {'User-Agent': 'Mozilla/5.0'}
#     request = Request(page_url, headers=hdr)
#     page = urlopen(request)
#     soup = BeautifulSoup(page, 'lxml')
#     # os.system('clear')
#     return soup








# url = 'https://shop.wakepark.by/snowboarding/snowboards/'

# page_doc = get_page_doc(url)
# pages_links = [
#     i.find_all('a') for i in page_doc.find_all("ul", class_="pagination")
#     ]
# result = list()
# result.append(url)
# for i in pages_links:
#     for j in i:
#         result.append(j.get('href'))
# pages_links = list(dict.fromkeys(result))


# categories = page_doc.find_all("a", class_="nav-link dropdown-toggle text-uppercase font-weight-bold")
# del categories[-1]
# categories.append(page_doc.find("a", class_='nav-link text-uppercase font-weight-bold px-1'))


# def get_categories(i):
    
#     category_name = i.text.strip()
#     skip_list = [
#         'Бренды', 'Акции', 'Подарочные сертификаты', 'О нас',
#         'Реквизиты', 'Преимущества', 'Таблица размеров', 'Обратная связь',
#         'Контакты', 'Регистрация', 'Авторизация', 'Показать все', 'Доставка и оплата'
#         ]
#     if category_name not in skip_list:
#         url = i.get('href')                
#         doc = get_page_doc(url)
#         sub_result = doc.find_all('a', class_='btn btn-light bg-white rounded-0 text-uppercase font-weight-bold px-3 py-2 mx-2 mb-3')
#         """Searching for sub_cagories object in row above. Result contains tag <a>."""
#         links_to_subcategories = [i.get('href') for i in sub_result]
#         titles = [i.text.strip() for i in sub_result] # get titles of categories
#         return (category_name, dict(zip(titles, links_to_subcategories)))



# with Pool(10) as p:
#     result = p.map(get_categories, categories)

# main_res = dict()
# for i in result:
#     main_res[i[0]] = i[1]

# # pages_links = [i.get('href') for i in pages_links]
# print(pages_links)
# containers = list()
# for link in pages_links:
#     page_doc = get_page_doc(link)
#     containers += page_doc.find_all("div", class_="border-0 rounded-0 h-100 product-card")


# def parse_containers(container):
#     link = container.find('a').get('href')
#     title = container.find('img').get('alt').strip()
#     if title != 'Скидочная карта SHOP.WAKEPARK.BY':
#         try:
#             doc = get_page_doc(link)
#         except:
#             pass
#         prices = doc.find('div', class_='p-price h2').text.strip()
#         prices = prices.split(' ')
#         if len(prices) == 2:
#             if 'BYN' not in prices[1]:
#                 prices[0] = prices[0].replace('BYN', '') + prices[1]
#                 del prices[1]
#             else:
#                 prices[0] = prices[0].replace('BYN', '')
#                 del prices[1]
#         elif len(prices) == 3:
#             for i in prices:
#                 if '\xa0\xa0' in i:
#                     prices[1] = prices[1].replace("\t", "").replace("\n", "").replace('\xa0\xa0','').replace('BYN','')
#                     del prices[2]
#                     break
#             else:
#                 prices[0] += prices[1]
#                 del prices[1]
#                 del prices[1]
                
#         elif len(prices) == 4:
#             prices[1] = prices[1].replace("\t", "").replace("\n", "").replace('\xa0\xa0','').replace('BYN','') + prices[2]
#             del prices[2]
#             del prices[2]
#         else:
#             prices[0] += prices[1]
#             prices[2] = prices[2].replace("\t", "").replace("\n", "").replace('\xa0\xa0','').replace('BYN','') + prices[3]
#             del prices[1]
#             del prices[3]
#             del prices[2]
#         print(title, prices, link)
#         return [title, [float(i[0:-1]) for i in prices], link]

# last_res = list()
# with Pool(10) as p:
#     last_res += p.map(parse_containers, containers)


# for i in last_res:
#     print(i,'\n\n\n')