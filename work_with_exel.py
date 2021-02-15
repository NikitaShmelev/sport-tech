import datetime
import os
import xlsxwriter


def init_file_name(user):
    file_name = f'{user.selected_shop}/{user.selected_category}/{user.selected_sub_category}.xlsx'
    return file_name