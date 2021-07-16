import time
import os

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from telegram import Bot, Update
from telegram.utils.request import Request
from logging import getLogger

from bot_token import bot_token
from debug_for_bot import debug_requests, load_config
from keyboards_for_bot import available_shops_keyboard, available_categories_keyboard, back_button_logic
from some_data import shops, User
from parsing import Parsing

config = load_config(getLogger(__name__))
users = dict()
parsing = Parsing()

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
        if not users[chat_id].start_parse:
            if text_data in shops.keys():
                users[chat_id].selected_shop = text_data
                shop = users[chat_id].selected_shop
                users[chat_id].categories = parsing.get_categories(
                        parsing.get_page_doc(shops[text_data]), shops[shop]
                    )
                update.effective_chat.send_message(
                    text='Select category',
                    reply_markup=available_categories_keyboard(
                            users[chat_id].categories, True if users[chat_id].selected_category else False
                        )
                )
            elif text_data == 'BACK':
                users[chat_id] = back_button_logic(users[chat_id], update)
            elif text_data in users[chat_id].categories.keys():
                # if users[chat_id].selected_shop == 'Darsi':
                #     users[chat_id] = shops[users[chat_id].selected_shop].parse_category(
                #         users[chat_id].categories[text_data], text_data
                #     )
                # else:
                users[chat_id].selected_category = text_data
                users[chat_id].selected_sub_category = True
                update.effective_chat.send_message(
                    text='Select something',
                    reply_markup=available_categories_keyboard(users[chat_id].categories[text_data], True if users[chat_id].selected_category else False),
                )
            elif text_data == 'ALL CATEGORY':
                pass
            elif users[chat_id].selected_category and text_data in users[chat_id].categories[users[chat_id].selected_category].keys():
                users[chat_id].selected_sub_category = text_data
                users[chat_id] = parsing.parse_logic(shops[users[chat_id].selected_shop], users[chat_id], update)
                parsing.file_logic(users[chat_id], update)
                users[chat_id].__init__(chat_id=users[chat_id].chat_id)
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