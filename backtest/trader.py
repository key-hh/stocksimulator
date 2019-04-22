'''
Created on 2017. 2. 14.

@author: Administrator
'''

#trader 
class Trade:
        
    def __init__(self):
        self.initial_capital = 0
        self.commission = 0
        self.tradeItem = []
        
    def initialize(self):
        pass
    
    def handle_data(self, data):
        pass 
    
    def order(self, data, amount, div):
       
        if amount > 0 and data.my_amount < amount :
            data.act_amount = data.my_amount
            data.my_amount = 0
            data.order_amount = amount
        else :
            data.order_amount = amount
            data.act_amount = amount
            data.my_amount = data.my_amount - data.act_amount
       
        
        if div == "O":
            data.after_capital = data.current_capital + (data.open_price * data.act_amount)
            data.deal = data.open_price * data.act_amount            
        if div == "C":
            data.after_capital = data.current_capital + (data.close_price * data.act_amount)
            data.deal = data.close_price * data.act_amount
     
        data.after_capital = data.after_capital - (data.act_amount * self.commission)
     
     
    def historyItem(self, item, index):
        hist = []
        for idx in range(1,index) :
            hist.append(getattr(self.tradeItem[-idx],item))
        return hist
    
    def history(self, index):
        hist = []
        for idx in range(1,index) :
            hist.append(self.tradeItem[-idx])
        return hist
    
    def getInitialCapital(self):
        return self.initial_capital 
        
    def getCommission(self):
        return self.commission
        
    def setInitialCapital(self, cap):
        self.initial_capital = cap 
        
    def setCommission(self, commission):
        self.commission = commission 
         
    def appendItem(self, item):
        self.tradeItem.append(item)

#trading unit item
class TradeItem:
    def __init__(self, date, open_price, close_price, min_price, max_price, volume, predict_open_price, predict_price, current_capital,my_amount):
        self.date = date
        self.open_price = open_price
        self.close_price =close_price
        self.min =min
        self.min_price = min_price
        self.max_price = max_price
        self.volume = volume
        self.predict_open_price = predict_open_price
        self.predict_price = predict_price
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
    
    
        
        
        