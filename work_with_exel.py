import datetime
import os
import xlsxwriter
from openpyxl import load_workbook

def __create__(name):
    try:
        os.mkdir(name)
    except FileExistsError:
        pass


def create_folders(shop, category, keys):
    __create__(f'{shop}/{category}')
    __create__(f'{shop}/{category}/ALL')
    if keys:
        for folder_name in keys:
            __create__(f'{shop}/{category}/{folder_name}')

    


def init_file_name(user):
    file_name = f'{user.selected_shop}/{user.selected_category}/{user.selected_sub_category}'
    return file_name


def create_exel_file(file_name):
    workbook = xlsxwriter.Workbook(file_name)
    return workbook


def init_worksheet(workbook, sheet_name, compare=False):
    worksheet = workbook.add_worksheet(sheet_name)
    worksheet.set_column(0, 5, 25)
    worksheet.write(1, 0, 'Category')
    worksheet.write(1, 1, 'Title')
    
    if compare:
        worksheet.write(1, 2, 'Current price') # ADD DATE
        worksheet.write(1, 3, 'Old price')   
    else:
        worksheet.write(1, 3, 'Current price')
        worksheet.write(1, 2, 'Old price')   
    
    worksheet.write(1, 4, 'Size/Sex')
    worksheet.write(1, 5, 'Page url')
    worksheet.write(0, 2, str(datetime.date.today()))
    
    return worksheet


def record_data(shop, data_for_record, workbook, 
                worksheet, selected_category, row=2, col=0):
    print(selected_category)
    # row = 2
    # col = 0
    if shop == 'FAMILY BOARDSHOP':
        for record in data_for_record:
            # record[0] - title
            # record[1] - prices. Can contain old and new or only current price
            # record[2] - page_url
             # category
            if record:
                worksheet.write(row, col, selected_category)
                worksheet.write(row, col + 1, record[0]) # title
                if len(record[1]) == 2:
                    worksheet.write(row, col + 3, record[1][0]) # current price
                    worksheet.write(row, col + 2, record[1][1]) # old price 
                else:
                    worksheet.write(row, col + 2, record[1][0])
                worksheet.write(row, col + 5, record[2]) # url
                row += 1
        
    elif shop == 'Dominant':
        for record in data_for_record:
            print(selected_category, record)
            for size in record[-2]:
                worksheet.write(row, col, selected_category) # category
                worksheet.write(row, col + 1, record[0]) # title
                worksheet.write(row, col + 3, record[1]) # current price
                worksheet.write(row, col + 2, record[2]) # old price 
                worksheet.write(row, col + 4, size) # size
                worksheet.write(row, col + 5, record[-1]) # url
                row += 1
    elif shop == 'Rollershop':
        print(type(data_for_record))
        for record in data_for_record:
            # print(type(record), record)
            if len(record) == 5:
                for size in record[3]:
                    # print(type(size), size)
                    if size != '--- Выберите ---' and len(record) > 1:
                        worksheet.write(row, 0, record[0]) # category  
                        worksheet.write(row, col + 1, record[1]) # title
                        if record[2][1]:
                            worksheet.write(row, col + 3, record[2][0]) # current_price
                            worksheet.write(row, col + 2, record[2][1]) # current_price
                        else:
                            worksheet.write(row, col + 3, record[2][0]) # current_price
                        worksheet.write(row, col + 4, size) # size
                        worksheet.write(row, col + 5, record[4]) # link
                        row += 1
            else:
                worksheet.write(row, col, record[0]) # category  
                worksheet.write(row, col + 1, record[1]) # title
                worksheet.write(row, col + 3, record[2]) # price
                # add old price 
                # worksheet.write(row, col + 3, record[2]) # size
                worksheet.write(row, col + 5, record[3]) # link
                row += 1
    return row


def get_old_file(path):
    files_list = os.listdir(path)
    if len(files_list):
        return files_list[0]
    else:
        return False


def get_keys_and_values_from_file(file_name):
    wb = load_workbook(file_name)
    ws = wb.active
    result = dict()
    for row in ws.iter_rows():
        sub_res = list()
        for cell in row:
            if cell.value == 'Category':
                break
            else:
                sub_res.append(cell.value)
        else:
            result[sub_res[0]] = dict(key=sub_res[1], value=sub_res[2:3])
            print(f'{result[sub_res[0]]}')
    return result


def get_compared_file(old_file, new_file):
    new_file_dict = {
        line[1]:line[2] for line in new_file 
    }
    print(new_file.keys())


def get_column_for_prices(path):
    pass