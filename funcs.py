from bs4 import BeautifulSoup
import requests as req
import lxml
from urllib.request import Request, urlopen


def get_page_doc(page_url):
    # resp = req.get(page_url)
    # soup = BeautifulSoup(resp.text, 'lxml')
    
    site = page_url
    hdr = {'User-Agent': 'Mozilla/5.0'}
    req = Request(site, headers=hdr)
    page = urlopen(req)
    soup = BeautifulSoup(page, 'lxml')
    return soup


# chromedriver = '/home/nshmelyov/.wdm/drivers/chromedriver/linux64/84.0.4147.30/chromedriver'
#     options = webdriver.ChromeOptions()
#     options.add_argument('headless')  # для открытия headless-браузера
#     browser = webdriver.Chrome(executable_path=chromedriver, chrome_options=options)
#     browser.get(page_url)
#     requiredHtml = browser.page_source
#     soup = BeautifulSoup(requiredHtml, 'html5lib')
