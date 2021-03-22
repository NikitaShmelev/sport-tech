import datetime
import os
import xlsxwriter

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
    worksheet.write(0, 0, 'Category')
    worksheet.write(0, 1, 'Title')
    
    if compare:
        worksheet.write(0, 2, 'Current price') # ADD DATE
        worksheet.write(0, 3, 'Old price')   
    else:
        worksheet.write(0, 2, 'Current price')
        worksheet.write(0, 3, 'Old price')   
    
    worksheet.write(0, 4, 'Size/Sex')
    worksheet.write(0, 5, 'Page url')
    worksheet.write(0, 6, str(datetime.date.today()))
    
    return worksheet


def record_data(shop, data_for_record, workbook, 
                worksheet, selected_category):
    print(selected_category)
    row = 1
    col = 0
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
                    worksheet.write(row, col + 2, record[1][0]) # current price
                    worksheet.write(row, col + 3, record[1][1]) # old price 
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
                worksheet.write(row, col + 2, record[1]) # current price
                worksheet.write(row, col + 3, record[2]) # old price 
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
                        worksheet.write(row, col, record[0]) # category  
                        worksheet.write(row, col + 1, record[1]) # title
                        if record[2][1]:
                            worksheet.write(row, col + 2, record[2][0]) # current_price
                            worksheet.write(row, col + 3, record[2][1]) # current_price
                        else:
                            worksheet.write(row, col + 2, record[2][0]) # current_price
                        worksheet.write(row, col + 4, size) # size
                        worksheet.write(row, col + 5, record[4]) # link
                        row += 1
            else:
                worksheet.write(row, col, record[0]) # category  
                worksheet.write(row, col + 1, record[1]) # title
                worksheet.write(row, col + 2, record[2]) # price
                # add old price 
                # worksheet.write(row, col + 3, record[2]) # size
                worksheet.write(row, col + 5, record[3]) # link
                row += 1
    # return row


def get_old_file(path):
    return os.listdir(path)[0]


def get_keys_and_values_from_file(file_name):
    pass