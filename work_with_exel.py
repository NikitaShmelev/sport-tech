import datetime
import os
import xlsxwriter


def init_file_name(user):
    file_name = f'{user.selected_shop}/{user.selected_category}/{user.selected_sub_category}.xlsx'
    return file_name


def create_exel_file(file_name):
    workbook = xlsxwriter.Workbook(file_name)
    worksheet = workbook.add_worksheet()
    worksheet.set_column(0, 5, 25)
    worksheet.write(0, 0, 'Category')
    worksheet.write(0, 1, 'Title')
    worksheet.write(0, 2, 'Current price')
    worksheet.write(0, 3, 'Old price')
    worksheet.write(0, 4, 'Size/Sex')
    worksheet.write(0, 5, 'Page url')
    return workbook, worksheet


def record_data(shop, data_for_record, workbook, 
                worksheet, selected_category, row):
    print(selected_category)
    
    col = 0
    if shop == 'FAMILY BOARDSHOP':
        for record in data_for_record:
            # record[0] - title
            # record[1] - prices. Can contain old and new or only current price
            # record[2] - page_url
            worksheet.write(row, col, selected_category) # category
            if record:
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
            print(record)
            for size in record[-2]:
                worksheet.write(row, col, selected_category) # category
                worksheet.write(row, col + 1, record[0]) # title
                worksheet.write(row, col + 2, record[1]) # current price
                worksheet.write(row, col + 3, record[2]) # old price 
                worksheet.write(row, col + 4, size) # size
                worksheet.write(row, col + 5, record[-1]) # url
                row += 1
    elif shop == 'Rollershop':
        for record in data_for_record: 
                
            if len(record) == 4:
                for size in record[2]:
                    if size != '--- Выберите ---' and len(record) > 1:
                        worksheet.write(row, col, selected_category) # category  
                        worksheet.write(row, col + 1, record[0]) # title
                        worksheet.write(row, col + 2, record[1]) # price
                        # add old price
                        worksheet.write(row, col + 4, size) # size
                        worksheet.write(row, col + 5, record[3]) # link
                        row += 1
            else:
                worksheet.write(row, col, selected_category) # category  
                worksheet.write(row, col + 1, record[0]) # title
                worksheet.write(row, col + 2, record[1]) # price
                # add old price 
                # worksheet.write(row, col + 3, record[2]) # size
                worksheet.write(row, col + 5, record[2]) # link
                row += 1
    return row