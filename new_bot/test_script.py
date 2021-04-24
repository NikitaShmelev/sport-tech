from bs4 import BeautifulSoup
import requests as req
import lxml
from urllib.request import Request, urlopen
from multiprocessing import Pool
import os
import xlsxwriter
from openpyxl import load_workbook
import sys
from parsing import Parsing
from dominant import Dominant
from rollershop import Rollershop
from wakepark import Wakepark
parsing = Parsing()
sys.setrecursionlimit(100000)

shops = {
        'Dominant': Dominant(),
        'FAMILY BOARDSHOP': Wakepark(),
        'Rollershop': Rollershop(),
    }

# get main_page
for name in shops.keys():
    print(name)
    page_doc = parsing.get_page_doc(shops[name])
    print(page_doc)
