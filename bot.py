import xlsxwriter

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from telegram import ReplyKeyboardRemove, Bot, Update
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup
from telegram.utils.request import Request

import datetime
import os
from logging import getLogger
import time
import openpyxl

from bot_token.bot_token import bot_token
from debug_for_bot import debug_requests, load_config
from keyboards_for_bot import available_shops_keyboard, available_categories_keyboard
from some_data import shops, User
from parsing import get_page_doc, get_categories, parse_category
from work_with_exel import init_file_name, record_data, create_exel_file, create_folders, init_worksheet, \
    get_old_file, get_keys_and_values_from_file, get_compared_file, get_last_colunm_index, add_prices_worksheets, record_prices, \
    record_old_data
from compare import get_indexes_for_record

config = load_config(getLogger(__name__))
users = dict()

@debug_requests
def do_start(update: Update, context=CallbackContext):
    chat_id = update.message.chat_id
    if chat_id not in users.keys():
        users[chat_id] = User(chat_id)
        update.effective_chat.send_message(
            text='Select shop',
            reply_markup=available_shops_keyboard()
            )
    else:
        if users[chat_id].start_parse:
            update.effective_chat.send_message(
                text='Проше не тыкать ничего. Сейчас я не просто думаю, ' + 
                   'но ещё и среагировать могу. Не испытывайте судьбу плес.' +
                   ' Создатель поленился сейчас прописывать все аспекты моего поведения. ' +
                   'Всё потом. Зато многопоточка' 
                )
        else:
            users[chat_id].selected_shop = None
            users[chat_id].categories = None
            users[chat_id].selected_category = None
            update.effective_chat.send_message(
                text='Select shop',
                reply_markup=available_shops_keyboard()
                )
    
    


@debug_requests
def get_text(update: Update, context: CallbackContext):
    text_data = update.message.text
    chat_id = update.message.chat_id
    start_time = time.time()
    if chat_id in users.keys():
        # print(text_data, users[chat_id].categories.keys())
        if not users[chat_id].start_parse:
            if text_data in shops.keys():
                print(text_data)
                users[chat_id].selected_shop = text_data
                page_doc = get_page_doc(shops[text_data])
                users[chat_id].categories = get_categories(page_doc, users[chat_id].selected_shop)
                update.effective_chat.send_message(
                    text='Select category',
                    reply_markup=available_categories_keyboard(
                            users[chat_id].categories, True if users[chat_id].selected_category else False
                        )
                )
            elif text_data == 'BACK':
                if users[chat_id].selected_sub_category:
                    users[chat_id].selected_sub_category = False
                    users[chat_id].selected_category == None
                    update.effective_chat.send_message(
                        text='Select category',
                        reply_markup=available_categories_keyboard(
                                    users[chat_id].categories, True if users[chat_id].selected_category else False
                                    )
                    )
                elif users[chat_id].selected_category:
                    users[chat_id].selected_category == None
                    print(users[chat_id].selected_category)
                    update.effective_chat.send_message(
                        text='Select shop',
                        reply_markup=available_shops_keyboard()
                        )
                elif not users[chat_id].selected_category and users[chat_id].selected_shop:
                    users[chat_id].selected_shop == None
                    update.effective_chat.send_message(
                        text='Select shop',
                        reply_markup=available_shops_keyboard()
                    )
                    
            elif text_data in users[chat_id].categories.keys():
                users[chat_id].selected_category = text_data
                users[chat_id].selected_sub_category = True
                update.effective_chat.send_message(
                    text='Select something',
                    reply_markup=available_categories_keyboard(users[chat_id].categories[text_data], True if users[chat_id].selected_category else False),
                )
            elif text_data == 'ALL CATEGORY':
               
                update.effective_chat.send_message(
                    text='So be it. Please w8 some time, you can drink coffee. '
                        'I will send result soonest as possible.',
                    reply_markup=ReplyKeyboardRemove()
                )
                # path = f'{users[chat_id].selected_shop/users[chat_id].selected_category}'
                selected_category = users[chat_id].selected_category
                file_name = init_file_name(users[chat_id]) + 'ALL_CATEGORY.xlsx' # if python >= 3.8
                start_time = time.time()
                create_folders(users[chat_id].selected_shop, users[chat_id].selected_category, False)
                workbook = create_exel_file(file_name)
                worksheet = init_worksheet(workbook, users[chat_id].selected_category)
                row = 2
                for category in users[chat_id].categories[selected_category]:
                    compare = False
                    # check files
                    result = parse_category(
                        users[chat_id].selected_shop,
                        users[chat_id].categories[selected_category][category],
                        category
                        )
                    # worksheet = init_worksheet(workbook, category)
                    row = record_data(
                        users[chat_id].selected_shop,
                        result, workbook, worksheet, category, row
                    )

                workbook.close()
                file = open(f'{file_name}', 'rb') # if python >= 3.8
                update.effective_chat.bot.send_document(
                    chat_id=chat_id,
                    document=file,
                    reply_markup=available_categories_keyboard(users[chat_id].categories, True if users[chat_id].selected_category else False),
                )
                file.close()
                # os.remove(file_name)
            elif users[chat_id].selected_category and text_data in users[chat_id].categories[users[chat_id].selected_category].keys():
                
                users[chat_id].selected_sub_category = text_data
                keys = users[chat_id].categories[users[chat_id].selected_category].keys()
                create_folders(users[chat_id].selected_shop, users[chat_id].selected_sub_category, keys)
                path = init_file_name(users[chat_id])
                
                old_file = get_old_file(path)
                print(old_file, path)
                old_file_values = get_keys_and_values_from_file(f'{path}/{old_file}') if old_file else False

                # for key in old_file_values.keys():
                #     print(key, old_file_values[key])
                # print(old_file_values.keys())
                new_file = f'{path}/{users[chat_id].selected_sub_category}.xlsx'
                # column = get_column_for_prices(get_old_file(path))


                update.effective_chat.send_message(
                    text='Проше не тыкать ничего. Сейчас я не просто думаю, ' + 
                            'но ещё и среагировать могу. Не испытывайте судьбу плес.' +
                            ' Создатель поленился сейчас прописывать все аспекты моего поведения. ' +
                            'Всё потом. Зато многопоточка' ,
                    reply_markup=ReplyKeyboardRemove()
                )
                
                
                users[chat_id].result = None
                users[chat_id].result = parse_category(
                        users[chat_id].selected_shop,
                        users[chat_id].categories[users[chat_id].selected_category][text_data],
                        users[chat_id].selected_sub_category
                        )
                
                if old_file_values:
                    
                    last_column = get_last_colunm_index(f'{path}/{old_file}')
                    result, new_items = get_indexes_for_record(users[chat_id].result, old_file_values, users[chat_id].selected_shop)

                    workbook = create_exel_file(new_file)
                    worksheet = init_worksheet(workbook, users[chat_id].selected_sub_category)
                    workbook, worksheet = add_prices_worksheets(workbook, worksheet, last_column)

                    row = record_old_data(workbook, worksheet, old_file_values)
                    
                    record_prices(workbook, worksheet, result, last_column, users[chat_id].selected_shop)
                    print(new_items, 'new_items')
                    workbook.close()
                    del workbook, worksheet, last_column 
                else:
                    workbook = create_exel_file(new_file)
                    worksheet = init_worksheet(workbook, users[chat_id].selected_sub_category)

                    record_data( 
                        users[chat_id].selected_shop,
                        users[chat_id].result, workbook, worksheet, 
                        users[chat_id].selected_sub_category
                    ) # first record
                    workbook.close()


                    del workbook, worksheet
                users[chat_id].start_parse = False
                users[chat_id].selected_sub_category = False
                users[chat_id].result = None

                # if old_file:
                #     compared_file = get_compared_file(old_file=old_file, new_file=new_file)

                file = open(f'{new_file}', 'rb') # if python >= 3.8
                update.effective_chat.bot.send_document(
                    chat_id=chat_id,
                    document=file,
                    reply_markup=available_categories_keyboard(users[chat_id].categories, True if users[chat_id].selected_category else False),
                )
                file.close()
                print(time.time() - start_time, 'result time')
            else:
                return do_start(update, context)
        else:
            return do_start(update, context)
    else:
        return do_start(update, context)
        


@debug_requests
def main():
    for i in shops:
        try:
            os.mkdir(i)
        except:
            pass
    request = Request(
        connect_timeout=0.5,
        read_timeout=1.0,
	    )
    bot = Bot(
        # request=request,
        token=bot_token,
        )
    updater = Updater(
        bot=bot,
        use_context=True
        )
    print(bot.get_me())
    start_handler = CommandHandler(
        "start",
        do_start
        )
    
    # Message handlers
    text_message_handler = MessageHandler(
        Filters.text,
        get_text
        )
    
    # dispatchers
    updater.dispatcher.add_handler(text_message_handler)
    updater.dispatcher.add_handler(start_handler)
    

    updater.start_polling()
    updater.idle()





if __name__ == '__main__':
    main()