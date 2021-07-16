import os

from work_with_exel import Exel_Work
from telegram import ReplyKeyboardRemove, chat
from keyboards_for_bot import available_categories_keyboard
from work_with_exel import Exel_Work


class Parsing():

    
    def get_page_doc(self, shop_obj, url=None):
        return shop_obj.get_page_doc()


    def get_categories(self, page_doc, shop_obj):
        return shop_obj.get_categories(page_doc)


    def __create_filename__(self, user, ALL=False):
        keys = user.categories[user.selected_category].keys()
        self.__create_folders__(user.selected_shop, user.selected_category, keys)
        new_file = Exel_Work().init_file_name(user, ALL)
    
        # new_file = f'{path}/{user.selected_sub_category}.xlsx'
        return new_file
    

    def parse_logic(self, shop_obj, user, update):
        update.effective_chat.send_message(
                    text='Prosze poczekać! Душу "' 
                          f'{user.selected_sub_category}"' ,
                    reply_markup=ReplyKeyboardRemove()
                )
        user.result = shop_obj.parse_category(
            user.categories[user.selected_category][user.selected_sub_category],
            user.selected_sub_category
            )
        return user
    
    def file_logic(self, user, update, ALL=False):
        
        new_file = self.__create_filename__(user, ALL)
        workbook = Exel_Work().create_exel_file(new_file)
        worksheet = Exel_Work().init_worksheet(workbook, user.selected_sub_category, compare=False, ALL=True)

        workbook, worksheet = Exel_Work().record_data( 
            user.result, workbook, worksheet, 
        ) # first record
        workbook.close()
        file = open(new_file, 'rb')
        update.effective_chat.bot.send_document(
                    chat_id=user.chat_id,
                    document=file,
                    reply_markup=available_categories_keyboard(
                        user.categories, True if user.selected_category else False),
                )
        file.close()


    def __create__(self, name):
        try:
            os.mkdir(name)
        except FileExistsError:
            pass


    def __create_folders__(self, shop, category, keys):
        self.__create__(f'{shop}/{category}')
        self.__create__(f'{shop}/{category}/ALL')
        if keys:
            for folder_name in keys:
                self.__create__(f'{shop}/{category}/{folder_name}')