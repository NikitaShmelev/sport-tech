from telegram import KeyboardButton, ReplyKeyboardMarkup
from parsing import get_page_doc
from some_data import shops



def available_shops_keyboard():
    keyboard = [
        [KeyboardButton(i)] for i in shops.keys()
    ]
    
    
    return ReplyKeyboardMarkup(
        keyboard=keyboard,
        resize_keyboard=True,
    )


def available_categories_keyboard(categories):

    keyboard = [
        [KeyboardButton(i)] for i in categories.keys()
    ]
    return ReplyKeyboardMarkup(
        keyboard=keyboard,
        resize_keyboard=True,
    )