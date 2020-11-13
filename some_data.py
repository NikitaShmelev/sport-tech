class User():
    def __init__(self, chat_id=None):
        self.chat_id = chat_id
        self.selected_shop = None
        self.categories = dict()
        self.start_parse = False


shops = {
        'FAMILY BOARDSHOP': 'https://shop.wakepark.by/',
    }