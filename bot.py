import xlsxwriter

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from telegram import ReplyKeyboardRemove, Bot, Update
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup
from telegram.utils.request import Request

import datetime
import os
from logging import getLogger
import time


from debug_for_bot import debug_requests, load_config
from keyboards_for_bot import available_shops_keyboard, available_categories_keyboard
from some_data import shops, User
from parsing import get_page_doc, get_categories_stihiya, parse_category_stihiya

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
                text='I\'m thinking, w8 pls'
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
                users[chat_id].selected_shop = text_data
                page_doc = get_page_doc(shops[text_data])
                users[chat_id].categories = get_categories_stihiya(page_doc)
                update.effective_chat.send_message(
                    text='Select category',
                    reply_markup=available_categories_keyboard(users[chat_id].categories)
                )
            elif text_data in users[chat_id].categories.keys():
                users[chat_id].selected_category = text_data
                update.effective_chat.send_message(
                    text='Select something',
                    reply_markup=available_categories_keyboard(users[chat_id].categories[text_data])
                )
            
            elif text_data in users[chat_id].categories[users[chat_id].selected_category].keys():
                users[chat_id].start_parse = True
                update.effective_chat.send_message(
                    text='So be it. Please w8 some time, you can drink coffee. '
                        'I will send result soonest as possible.',
                    reply_markup=ReplyKeyboardRemove()
                )
                print(users[chat_id].categories[users[chat_id].selected_category][text_data])

                result = parse_category_stihiya(users[chat_id].categories[users[chat_id].selected_category][text_data])
                users[chat_id].start_parse = False

                file_name = f'{text_data} {datetime.date.today()}.xlsx' # if python >= 3.8
                # file_name = text_data + str(datetime.date.today()) + '.xlsx'

                workbook = xlsxwriter.Workbook(file_name)
                worksheet = workbook.add_worksheet()
                worksheet.write(0, 0, 'Title')
                worksheet.write(0, 1, 'New price')
                worksheet.write(0, 2, 'Old price')
                worksheet.write(0, 3, 'Page url')
                row = 1
                col = 0
                for record in result:
                    # record[0] - title
                    # record[1] - prices. Can contain old and new or only current price
                    # record[2] - page_url
                    worksheet.write(row, col, record[0])
                    if len(record[1]) == 2:
                        worksheet.write(row, col + 1, record[1][0])
                        worksheet.write(row, col + 2, record[1][1])
                    else:
                        worksheet.write(row, col + 1, record[1][0])
                    worksheet.write(row, col + 3, record[2])
                    row += 1
                workbook.close()
                file = open(f'{file_name}', 'rb') # if python >= 3.8
                # file = open(file_name, 'rb')
                update.effective_chat.bot.send_document(
                    chat_id=chat_id,
                    text='Enjoi',
                    document=file,
                    reply_markup=available_categories_keyboard(users[chat_id].categories),
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
    request = Request(
        connect_timeout=0.5,
        read_timeout=1.0,
	    )
    bot = Bot(
        # request=request,
        token='1468659694:AAGQQAo6QddW9E_TK5efCtdu8D6D19e-pxk',
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