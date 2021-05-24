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


    def parse_logic(self, shop_obj, user, update):
        keys = user.categories[user.selected_category].keys()
        print(keys)
        self.__create_folders__(user.selected_shop, user.selected_category, keys)
        path = Exel_Work().init_file_name(user)
        print(path)
        # old_file_values = get_keys_and_values_from_file(
        #     f'{path}/{get_old_file(path)}') if old_file else False
        new_file = f'{path}/{user.selected_sub_category}.xlsx'
        update.effective_chat.send_message(
                    text='Prosze poczekać!' ,
                    reply_markup=ReplyKeyboardRemove()
                )
        user.result = shop_obj.parse_category(
            user.categories[user.selected_category][user.selected_sub_category],
            user.selected_sub_category
            )
        update.effective_chat.send_message(
                text='DONE, w8 for file' ,
                )        
        
        
        old_file_values = False

        # if old_file_values:
        #     pass
        # else:
        print(new_file,'!!!!!!!!!!!!!!!!!!!!!!!!1', user.selected_sub_category)
        workbook = Exel_Work().create_exel_file(new_file)
        worksheet = Exel_Work().init_worksheet(workbook, user.selected_sub_category)

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
        return user


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