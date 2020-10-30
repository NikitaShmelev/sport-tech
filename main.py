
from openpyxl import Workbook, load_workbook

from stihiya import Stihiya

url_dominant = 'https://dominant.by/catalog/longboardandcruiser/longbordy-i-kruizery-v-sbore/'

Stihiya_shop = Stihiya()


workbook = load_workbook(filename='test.xlsx')
work_sheet = workbook.active



longboards = Stihiya_shop.get_longboards()

i = 3
for key in longboards.keys():
    work_sheet[f'A{i}'] = key
    work_sheet[f'C{i}'] = longboards[key]
    i += 1


workbook.save('test.xlsx')
