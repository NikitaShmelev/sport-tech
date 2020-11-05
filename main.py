
from openpyxl import Workbook, load_workbook

from shops import Stihiya, Dominant, FamilyBoardshop

url_dominant = 'https://dominant.by/catalog/longboardandcruiser/longbordy-i-kruizery-v-sbore/'

Stihiya_shop = Stihiya()
Dominant_shop = Dominant()
Family_boardshop = FamilyBoardshop()


workbook = load_workbook(filename='test.xlsx')
work_sheet = workbook.active
Family_boardshop.categories
Family_boardshop.get_exel(Family_boardshop.categories)

# longboards_stihiya = Stihiya_shop.get_longboards()

# i = 3
# for key in longboards_stihiya.keys():
#     work_sheet[f'A{i}'] = key
#     work_sheet[f'B{i}'] = 'NONE'
#     work_sheet[f'C{i}'] = longboards_stihiya[key]
#     work_sheet[f'D{i}'] = 'NONE'
#     i += 1

# # longboards_dominant = Dominant_shop.get_longboards()

workbook.save('test.xlsx')
