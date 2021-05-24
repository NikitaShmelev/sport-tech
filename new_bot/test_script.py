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
from darsi import Darsi
from rollershop import Rollershop
from wakepark import Wakepark
import urllib.request
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
import time
import keyboard
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
parsing = Parsing()
sys.setrecursionlimit(100000)

shops = {
        'Dominant': Dominant(),
        'FAMILY BOARDSHOP': Wakepark(),
        'Rollershop': Rollershop(),
        'Darsi': Darsi(),
    }

# # get main_page
# for name in shops.keys():
#     print(name)
    # page_doc = parsing.get_page_doc(shops[name])
#     print(page_doc)


page_doc = parsing.get_page_doc(shops['Darsi'])
categories = parsing.get_categories(page_doc, shops['Darsi'])

for key in categories.keys():
    url = categories[key]
    # print(categories[key])
    # page_doc = parsing.get_page_doc(shops['Darsi'], categories[key])
    # print(page_doc)
    # containers = page_doc.find_all('div', class_='js-product t-store__card t-col t-col_4 t-align_center  t-item t-animate t-animate_started')
    # r = req.get(categories[key], headers = {'User-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36'})
    # driver = webdriver.Chrome(ChromeDriverManager().install())
    driver = webdriver.Firefox(executable_path=GeckoDriverManager().install())
    driver.get(f'{url}')
    # while True:
    #     try:
    #         driver.find_element_by_xpath('//*[text()="Load more"]').click()
    #         time.sleep(2)
    #     except:
    #         # break
    #         # keyboard.press(
    #         #     'ctrl+s'
    #         # )
    #         # import pyautogui
    #         # pyautogui.press('f5') 
    #         # pyautogui.hotkey('ctrl', 's')
    #         # keyboard.press_and_release('ctrl+s')
    #         break
    action = ActionChains(driver)

    # perform the oepration
    
    action.key_down(Keys.CONTROL).send_keys('s').perform()
    
    # driver.find_element_by_xpath('//*[text()="Load more"]').click()
    # print(dir(driver))
    # print(driver.find_element_by_class_name('t-store__card__imgwrapper t-store__card__imgwrapper_original-ratio'))
    # os.remove('page.html')

    # urllib.request.urlretrieve (categories[key], "webpage.html")
    break