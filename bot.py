import xlsxwriter

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from telegram import ReplyKeyboardRemove, Bot, Update
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup
from telegram.utils.request import Request

import datetime
import os
from logging import getLogger
import time

from bot_token.bot_token import bot_token
from debug_for_bot import debug_requests, load_config
from keyboards_for_bot import available_shops_keyboard, available_categories_keyboard
from some_data import shops, User
from parsing import get_page_doc, get_categories, parse_category
from work_with_exel import init_file_name

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
                    reply_markup=available_categories_keyboard(users[chat_id].categories, True if users[chat_id].selected_category else False)
                )
            elif text_data == 'BACK':
                if users[chat_id].selected_sub_category:
                    users[chat_id].selected_sub_category = False
                    users[chat_id].selected_category == None
                    update.effective_chat.send_message(
                        text='Select category',
                        reply_markup=available_categories_keyboard(users[chat_id].categories, True if users[chat_id].selected_category else False)
                    )
                elif users[chat_id].selected_category:
                    users[chat_id].selected_category == None
                    print(users[chat_id].selected_category)
                    update.effective_chat.send_message(
                        text='Select shop',
                        reply_markup=available_shops_keyboard()
                        )
                elif users[chat_id].selected_category == None:
                    users[chat_id].selected_category == None
                    update.effective_chat.send_message(
                        text='Select category',
                        reply_markup=available_categories_keyboard(users[chat_id].categories, True if users[chat_id].selected_category else False)
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
                selected_category = users[chat_id].selected_category
                file_name = f'{selected_category}(FULL)_{datetime.date.today()}.xlsx' # if python >= 3.8
                
                if users[chat_id].selected_shop == 'FAMILY BOARDSHOP':
                    workbook = xlsxwriter.Workbook(file_name)
                    worksheet = workbook.add_worksheet()
                    worksheet.write(0, 0, 'Category')
                    worksheet.write(0, 1, 'Title')
                    worksheet.write(0, 2, 'New price')
                    worksheet.write(0, 3, 'Old price')
                    worksheet.write(0, 4, 'Page url')
                    row = 1
                    col = 0
                    start_time = time.time()
                    for category in users[chat_id].categories[selected_category]:
                        result = parse_category(
                            users[chat_id].selected_shop,
                            users[chat_id].categories[selected_category][category]
                            )                    
                        print(f'\n\n{category} is ready, start recording\n')
                        for record in result:
                            if record:
                                worksheet.write(row, col, category)
                                worksheet.write(row, col + 1, record[0])
                                if len(record[1]) == 2:
                                    worksheet.write(row, col + 2, record[1][0])
                                    worksheet.write(row, col + 3, record[1][1])
                                else:
                                    worksheet.write(row, col + 2, record[1][0])
                                worksheet.write(row, col + 4, record[2])
                                row += 1
                    workbook.close()
                elif users[chat_id].selected_shop == 'Dominant':
                    workbook = xlsxwriter.Workbook(file_name)
                    worksheet = workbook.add_worksheet()
                    worksheet.set_column(0, 5, 25)
                    worksheet.write(0, 0, 'Category')
                    worksheet.write(0, 1, 'Title')
                    worksheet.write(0, 2, 'Current price')
                    worksheet.write(0, 3, 'Old price')
                    worksheet.write(0, 4, 'Size/Sex')
                    worksheet.write(0, 5, 'Page url')
                    row = 1
                    col = 0
                    for category in users[chat_id].categories[selected_category]:
                        result = parse_category(
                            users[chat_id].selected_shop,
                            users[chat_id].categories[users[chat_id].selected_category][category]
                            )
                        print(f'\n\n{category} is ready, start recording\n')
                        for record in result:
                            for size in record[-2]:
                                worksheet.write(row, col, category) # category
                                worksheet.write(row, col + 1, record[0]) # title
                                worksheet.write(row, col + 2, record[1]) # current price
                                worksheet.write(row, col + 3, record[2]) # old price 
                                worksheet.write(row, col + 4, size) # size
                                worksheet.write(row, col + 5, record[-1]) # url
                                row += 1
                    workbook.close()
                elif users[chat_id].selected_shop == 'Rollershop':
                    workbook = xlsxwriter.Workbook(file_name)
                    worksheet = workbook.add_worksheet()
                    worksheet.set_column(0, 5, 25)
                    worksheet.write(0, 0, 'Category')
                    worksheet.write(0, 1, 'Title')
                    worksheet.write(0, 2, 'Price')
                    worksheet.write(0, 3, 'Size')
                    worksheet.write(0, 4, 'Page url')
                    row = 1
                    col = 0
                    for category in users[chat_id].categories[selected_category]:
                        result = parse_category(
                            users[chat_id].selected_shop,
                            users[chat_id].categories[users[chat_id].selected_category][category]
                            )
                        print(f'\n\n{category} is ready, start recording\n')
                        for record in result:
                            
                            if len(record) == 4:
                                for size in record[2]:
                                    if size != '--- Выберите ---' and len(record[2]) > 1:
                                        worksheet.write(row, col, category)
                                        worksheet.write(row, col + 1, record[0]) # title
                                        worksheet.write(row, col + 2, record[1]) # price
                                        worksheet.write(row, col + 3, size) # size
                                        worksheet.write(row, col + 4, record[3]) # link
                            else:
                                worksheet.write(row, col, category)
                                worksheet.write(row, col + 1, record[0]) # title
                                worksheet.write(row, col + 2, record[1]) # price
                                worksheet.write(row, col + 4, record[2]) # link
                            row += 1
                    workbook.close()
                file = open(f'{file_name}', 'rb') # if python >= 3.8
                update.effective_chat.bot.send_document(
                    chat_id=chat_id,
                    document=file,
                    reply_markup=available_categories_keyboard(users[chat_id].categories, True if users[chat_id].selected_category else False),
                )
                file.close()
                os.remove(file_name)
            elif text_data in users[chat_id].categories[users[chat_id].selected_category].keys():
                # users[chat_id].start_parse = True
                users[chat_id].selected_sub_category = text_data
                file_name = init_file_name(users[chat_id])
                users[chat_id].selected_sub_category = False
                
                update.effective_chat.send_message(
                    text='Проше не тыкать ничего. Сейчас я не просто думаю, ' + 
                            'но ещё и среагировать могу. Не испытывайте судьбу плес.' +
                            ' Создатель поленился сейчас прописывать все аспекты моего поведения. ' +
                            'Всё потом. Зато многопоточка' ,
                    reply_markup=ReplyKeyboardRemove()
                )
                
                if users[chat_id].selected_shop == 'FAMILY BOARDSHOP':
                    result = parse_category(
                        users[chat_id].selected_shop,
                        users[chat_id].categories[users[chat_id].selected_category][text_data]
                        )
                    workbook = xlsxwriter.Workbook(file_name)
                    worksheet = workbook.add_worksheet()
                    worksheet.set_column(0, 5, 25)
                    worksheet.write(0, 0, 'Title')
                    worksheet.write(0, 1, 'Current price')
                    worksheet.write(0, 2, 'Old price')
                    worksheet.write(0, 3, 'Size/Sex')
                    worksheet.write(0, 4, 'Page url')
                    row = 1
                    col = 0
                    for record in result:
                        # record[0] - title
                        # record[1] - prices. Can contain old and new or only current price
                        # record[2] - page_url
                        if record:
                            worksheet.write(row, col, record[0])
                            if len(record[1]) == 2:
                                worksheet.write(row, col + 1, record[1][0])
                                worksheet.write(row, col + 2, record[1][1])
                            else:
                                worksheet.write(row, col + 1, record[1][0])
                            worksheet.write(row, col + 4, record[2])
                            row += 1
                    workbook.close()
                elif users[chat_id].selected_shop == 'Dominant':
                    result = parse_category(
                        users[chat_id].selected_shop,
                        users[chat_id].categories[users[chat_id].selected_category][text_data]
                        )
                    workbook = xlsxwriter.Workbook(file_name)
                    worksheet = workbook.add_worksheet()
                    worksheet.set_column(0, 5, 25)
                    worksheet.write(0, 0, 'Title')
                    worksheet.write(0, 1, 'Current price')
                    worksheet.write(0, 2, 'Old price')
                    worksheet.write(0, 3, 'Size/Sex')
                    worksheet.write(0, 4, 'Page url')
                    row = 1
                    col = 0
                    for record in result:
                        for size in record[-2]:
                            worksheet.write(row, col, record[0]) # title
                            worksheet.write(row, col + 1, record[1]) # current price
                            worksheet.write(row, col + 2, record[2]) # old price 
                            worksheet.write(row, col + 3, size) # size
                            worksheet.write(row, col + 4, record[-1]) # url
                            row += 1
                    workbook.close()

                elif users[chat_id].selected_shop == 'Rollershop':
                    result = parse_category(
                        users[chat_id].selected_shop,
                        users[chat_id].categories[users[chat_id].selected_category][text_data]
                        )
                    workbook = xlsxwriter.Workbook(file_name)
                    worksheet = workbook.add_worksheet()
                    worksheet.set_column(0, 5, 25)
                    worksheet.write(0, 0, 'Title')
                    worksheet.write(0, 1, 'Current price')
                    worksheet.write(0, 2, 'Old price')
                    worksheet.write(0, 3, 'Size/Sex')
                    worksheet.write(0, 4, 'Page url')
                    row = 1
                    col = 0
                
                    for record in result:
                        
                        if len(record) == 4:
                            for size in record[2]:
                                if size != '--- Выберите ---' and len(record) > 1:
                                    worksheet.write(row, col, record[0]) # title
                                    worksheet.write(row, col + 1, record[1]) # price
                                    worksheet.write(row, col + 3, size) # size
                                    worksheet.write(row, col + 4, record[3]) # link
                                    row += 1
                        else:
                            worksheet.write(row, col, record[0]) # title
                            worksheet.write(row, col + 1, record[1]) # price
                            # worksheet.write(row, col + 3, record[2]) # size
                            worksheet.write(row, col + 4, record[2]) # link
                            row += 1
                                    
                    workbook.close()
                users[chat_id].start_parse = False
                
                

               
                file = open(f'{file_name}', 'rb') # if python >= 3.8
                update.effective_chat.bot.send_document(
                    chat_id=chat_id,
                    document=file,
                    reply_markup=available_categories_keyboard(users[chat_id].categories, True if users[chat_id].selected_category else False),
                )
                file.close()
                os.remove(file_name)
                print(time.time() - start_time, 'result time')
            else:
                return do_start(update, context)
        else:
            return do_start(update, context)
    else:
        return do_start(update, context)
        


@debug_requests
def main():
    for i in shops.keys():
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