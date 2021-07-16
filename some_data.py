from dominant import Dominant
from rollershop import Rollershop
from wakepark import Wakepark
from darsi import Darsi

class User():
    
    
    def __init__(self, chat_id=None):
        self.chat_id = chat_id
        self.selected_shop = None
        self.categories = dict()
        self.start_parse = False
        self.selected_category = None
        self.selected_sub_category = None
        self.result = None
        

shops = {
        'Dominant': Dominant(),
        'FAMILY BOARDSHOP': Wakepark(),
        'Rollershop': Rollershop(),
        # 'Darsi': Darsi(),
    }