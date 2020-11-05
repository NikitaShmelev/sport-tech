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
