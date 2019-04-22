'''
Created on 2017. 2. 14.

@author: Administrator
'''

from enum import Enum


# enum
class TradeDiv(Enum):
    CLOSE_BASE = 1
    OPEN_BASE = 2


# trader
class Trade:
    def __init__(self):
        self.idx = 0
        self.tradeItem = []
        self.__capital = 0
        self.__commission = 0
        
    def initialize(self, capital, commission):
        pass

    def handle_data(self, data):
        pass 
    
    def order(self, data, amount, div):
        if amount > 0 and data.my_amount < amount:
            data.act_amount = data.my_amount
            data.my_amount = 0
            data.order_amount = amount
        else:
            data.order_amount = amount
            data.act_amount = amount
            data.my_amount = data.my_amount - data.act_amount

        if div == TradeDiv.OPEN_BASE:
            data.after_capital = data.current_capital + (data.open_price * data.act_amount)
            data.deal = data.open_price * data.act_amount            
        if div == TradeDiv.CLOSE_BASE:
            data.after_capital = data.current_capital + (data.close_price * data.act_amount)
            data.deal = data.close_price * data.act_amount
     
        data.after_capital = data.after_capital - (data.act_amount * self.__commission)

    def history_item(self, item, index):
        hist = []
        for idx in range(1, index):
            hist.append(getattr(self.tradeItem[-idx], item))
        return hist
    
    def history(self, index):
        hist = []
        for idx in range(1,index) :
            hist.append(self.tradeItem[-idx])
        return hist
    
    def get_initial_capital(self):
        return self.__capital
        
    def get_commission(self):
        return self.__commission

    def set_initial_capital(self, capital):
        self.__capital = capital

    def set_commission(self, commission):
        self.__commission = commission
        
    def append_trade_item(self, item):
        self.tradeItem.append(item)

    def increase_index(self):
        self.idx += 1

    def get_index(self):
        return self.idx

# trading unit item
class TradeItem:
    def __init__(self, date, open_price, close_price, data, current_capital, my_amount):
        self.date = date
        self.open_price = open_price
        self.close_price = close_price
        self.data = data
        self.current_capital = current_capital
        self.after_capital = current_capital
        self.deal = 0
        self.order_amount = 0
        self.act_amount = 0
        self.my_amount = my_amount
        self.profit_rate = 0.0
        self.open_asset = 0.0
        self.close_asset = 0.0
        self.asset_open_profit_rate = 0.0
        self.asset_close_profit_rate = 0.0
