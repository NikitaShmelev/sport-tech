import datetime
import os
import xlsxwriter
from openpyxl import load_workbook

class Exel_Work():


    def init_file_name(self, user, ALL=False):
        if ALL:
            return f'{user.selected_shop}/{user.selected_category}/ALL/category_result.xlsx'
        else:
            return f'{user.selected_shop}/{user.selected_category}/{user.selected_sub_category}/{user.selected_sub_category}.xlsx'


    def get_old_file(self, path):
        files_list = os.listdir(path)
        if len(files_list):
            return files_list[0]
        else:
            return False

    
    def create_exel_file(self, file_name):
        workbook = xlsxwriter.Workbook(file_name)
        print(file_name)
        return workbook


    def init_worksheet(self, workbook, sheet_name, compare=False, ALL=False):
        if len(sheet_name) > 31:
            sheet_name = sheet_name[0:30]
        worksheet = workbook.add_worksheet('category_result' if ALL else sheet_name)
        worksheet.set_column(0, 10, 25)
        worksheet.write(1, 0, 'Category')
        worksheet.write(1, 1, 'Title')
        worksheet.write(1, 2, 'Current price')
        worksheet.write(1, 3, 'Old price')

        worksheet.write(1, 4, 'Size/Sex')

        worksheet.write(1, 5, 'Page url')

        # merge_format = workbook.add_format({
        #     'bold': 1,
        #     'align': 'center',
        #     'valign': 'vcenter',
        #     'fg_color': 'yellow'}
        #     )
        # worksheet.merge_range('E1:F1', str(datetime.date.today()), merge_format)
        
        return worksheet


    def record_data(self, data, workbook, worksheet):
        row = 2
        for record in data:
            if record['sizes']:
                for size in record['sizes']:
                    worksheet.write(row, 0, record['category'])
                    worksheet.write(row, 1, record['title'])
                    worksheet.write(row, 2, record['current_price'])
                    worksheet.write(row, 3, record['old_price'])
                    worksheet.write(row, 4, size)
                    worksheet.write(row, 5, record['url'])
                    row += 1
            else:
                worksheet.write(row, 0, record['category'])
                worksheet.write(row, 1, record['title'])
                worksheet.write(row, 2, record['current_price'])
                worksheet.write(row, 3, record['old_price'])
                worksheet.write(row, 5, record['url'])
                row += 1
        print('DONE!')
        return workbook, worksheet