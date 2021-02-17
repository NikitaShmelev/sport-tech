from bs4 import BeautifulSoup
import requests as req
import lxml
from urllib.request import Request, urlopen

def get_page_doc_rollershop(url):
    hdr = {'User-Agent': 'Mozilla/5.0'}
    request = req.get(url, headers=hdr)
    request.encoding
    soup = BeautifulSoup(request.content.decode('utf-8', 'ignore'), 'lxml')
    # try:
    #     os.system('clear')
    # except:
    #     os.system('cls')
    return soup
