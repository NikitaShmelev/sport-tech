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
    worksheet.set_column(0, 10, 25)
    worksheet.write(1, 0, 'Category')
    worksheet.write(1, 1, 'Title')
    worksheet.write(1, 2, 'Size/Sex')
    worksheet.write(1, 3, 'Page url')
    
    if compare:
        worksheet.write(1, 4, 'Old price')   
        worksheet.write(1, 5, 'Current price') 
    else:
        worksheet.write(1, 4, 'Old price')   
        worksheet.write(1, 5, 'Current price')

    # worksheet.write(0, 4, )
    merge_format = workbook.add_format({
        'bold': 1,
        'align': 'center',
        'valign': 'vcenter',
        'fg_color': 'yellow'}
        )
    worksheet.merge_range('E1:F1', str(datetime.date.today()), merge_format)
    
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
                    worksheet.write(row, col + 5, record[1][0]) # current price
                    worksheet.write(row, col + 4, record[1][1]) # old price 
                else:
                    worksheet.write(row, col + 5, record[1][0])
                worksheet.write(row, col + 3, record[2]) # url
                row += 1
        
    elif shop == 'Dominant':
        for record in data_for_record:
            for size in record[-2]:
                worksheet.write(row, col, selected_category) # category
                worksheet.write(row, col + 1, record[0]) # title
                worksheet.write(row, col + 5, record[1][0]) # current price
                worksheet.write(row, col + 4, record[1][1]) # old price 
                worksheet.write(row, col + 2, size) # size
                worksheet.write(row, col + 3, record[-1]) # url
                row += 1
    elif shop == 'Rollershop':
        for record in data_for_record:
            if len(record) == 5:
                for size in record[3]:
                    # print(type(size), size)
                    if size != '--- Выберите ---' and len(record) > 1:
                        worksheet.write(row, 0, record[0]) # category  
                        worksheet.write(row, col + 1, record[1]) # title
                        if record[2][1]:
                            worksheet.write(row, col + 5, record[2][0]) # current_price
                            worksheet.write(row, col + 4, record[2][1]) # old
                        else:
                            worksheet.write(row, col + 5, record[2][0]) # current_price
                        worksheet.write(row, 2, size) # size
                        worksheet.write(row, 3, record[4]) # link
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
    for row in enumerate(ws.iter_rows()):
        # print(row)
        sub_res = list()
        if row[0] not in [0, 1]:
            for cell in row[1]:
                # print(cell.value)
                if row[0] not in sub_res:
                    sub_res.append(row[0])
                sub_res.append(cell.value)
            result[sub_res[0]] = sub_res[1:]
        # print(result)
    return result


def get_compared_file(old_file, new_file):
    new_file_dict = {
        line[1]:line[2] for line in new_file 
    }
    print(new_file.keys())


def get_last_colunm_index(path):
    wb = load_workbook(path)
    ws = wb.active
    for row in enumerate(ws.iter_rows()):
        if row[0] == 1:
            return (len(row[1]))
    wb.close()


def add_prices_worksheets(workbook, worksheet, last_column):
    print('\n\n\n\n',last_column)
    worksheet.write(1, last_column, 'Old price')   
    worksheet.write(1, last_column + 1, 'Current price')
    merge_format = workbook.add_format({
        'bold': 1,
        'align': 'center',
        'valign': 'vcenter',
        'fg_color': 'yellow'}
        )
    worksheet.merge_range(0, last_column, 0, last_column + 1, str(datetime.date.today()), merge_format)
    return workbook, worksheet


def record_old_data(workbook, worksheet, data_for_record):
    row = 2
    for key in data_for_record.keys():
        record = data_for_record[key]
        for i in range(len(record)):
            if record[i] != None:
                worksheet.write(row, i, record[i])
        row += 1
    return row


def record_prices(workbook, worksheet, result, last_column, shop):
    print("record_prices")
    print(len(result), result)
    for record in result:
        if shop == 'Rollershop':
            if record[3][1]:
                worksheet.write(record[0], last_column, record[3][0])   
                worksheet.write(record[0], last_column + 1, record[3][1])
            else:
                worksheet.write(record[0], last_column + 1, record[3][0])
        elif shop == 'Dominant':
            worksheet.write(record[0], last_column, record[2][1])
            worksheet.write(record[0], last_column + 1, record[2][0])
        elif shop == 'FAMILY BOARDSHOP':
            
            if len(record[2]) == 2:
                worksheet.write(record[0], last_column, record[2][1])   
                worksheet.write(record[0], last_column + 1, record[2][0])
            else:
                worksheet.write(record[0], last_column + 1, record[2][0])