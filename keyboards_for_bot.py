from telegram import KeyboardButton, ReplyKeyboardMarkup
from some_data import shops



def available_shops_keyboard():
    keyboard = [
        [KeyboardButton(i)] for i in shops.keys()
    ]
    
    
    return ReplyKeyboardMarkup(
        keyboard=keyboard,
        resize_keyboard=True,
    )


def available_categories_keyboard(categories, check_choice):

    keyboard = [
        [KeyboardButton(i)] for i in categories.keys()
    ]
    
    keyboard.insert(0, [KeyboardButton('BACK')])

    if check_choice:
        
        keyboard.append(
            [KeyboardButton('ALL CATEGORY')]
        )
    
    return ReplyKeyboardMarkup(
        keyboard=keyboard,
        resize_keyboard=True,
    )


def back_button_logic(user, update):
    if user.selected_sub_category:
        user.selected_sub_category = False
        user.selected_category = None
        update.effective_chat.send_message(
            text='Select category',
            reply_markup=available_categories_keyboard(
                        user.categories, True if user.selected_category else False
                        )
        )
    elif user.selected_category:
        user.selected_category = None
        update.effective_chat.send_message(
            text='Select shop',
            reply_markup=available_shops_keyboard()
            )
    elif not user.selected_category and user.selected_shop:
        user.selected_shop = None
        update.effective_chat.send_message(
            text='Select shop',
            reply_markup=available_shops_keyboard()
        )
    return user