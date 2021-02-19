from bs4 import BeautifulSoup
import requests as req
import lxml
from urllib.request import Request, urlopen
# from multiprocessing import Pool
import sys
import os
import time
from dominant import dominant_categories, parse_category_dominant
from rollershop import rollershop_categories, parse_category_rollershop
from wakepark import wakepark_categories, parse_category_wakepark

sys.setrecursionlimit(100000)


def get_page_doc(page_url):
    hdr = {'User-Agent': 'Mozilla/5.0'}
    request = Request(page_url, headers=hdr)
    page = urlopen(request)
    soup = BeautifulSoup(page, 'lxml')
    # os.system('clear')
    return soup

def make_folders(result, shop):
    for key in result.keys():
        try:
            os.mkdir(f'./{shop}/{key}')
        except:
            pass
        for sub_key in result[key]:
            try:
                os.mkdir(f'./{shop}/{key}/{sub_key}')
            except:
                pass



def get_categories(page_doc, shop, result=dict()):
    if shop == 'FAMILY BOARDSHOP':
        result = wakepark_categories(page_doc)    
    elif shop == 'Rollershop':
        result = rollershop_categories(get_page_doc_rollershop('https://rollershop.by/'))
    elif shop == 'Dominant':
        result = dominant_categories(page_doc)
        
    make_folders(result, shop)
    return result


def get_page_doc_rollershop(url):
    hdr = {'User-Agent': 'Mozilla/5.0'}
    request = req.get(url, headers=hdr)
    request.encoding
    soup = BeautifulSoup(request.content.decode('utf-8', 'ignore'), 'lxml')
    return soup



def parse_category(shop, url, result = list()):

    if shop == 'FAMILY BOARDSHOP':
        result = parse_category_wakepark(url)

    elif shop == 'Rollershop':
        result = parse_category_rollershop(url)
        
    elif shop == 'Dominant':
        result = parse_category_dominant(url)
    return result