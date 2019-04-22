'''
Created on 2017. 2. 14.

@author: Administrator
'''
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from . import displayer
from . import trader

#backtesting manager
class BackTest:
   
    def __init__(self):
        pass
    
    def readData(self, path):
        print("data read start---")
        
        tempData = pd.read_csv(path)
        tempData = tempData[pd.notnull(tempData["datetime"])]
        #data index 
        tempData["date"] = tempData.datetime.map(lambda x : pd.to_datetime(x))
        self.data = tempData.set_index("date")
        
        print("data read end---")
        
    def getData(self):
        return self.data
    
    def getResultData(self):
        return self.resultData
    
    def setDisplayer(self, displayer):
        self.displayer = displayer
    
    def displayData(self):
        if self.displayer is None : 
            raise ValueError("display is none.")
        
        self.displayer.display(self.data)
    
    def displayResultData(self):
        if self.displayer is None : 
            raise ValueError("display is none.")
        
        self.displayer.displayResult(self.data, self.resultData)
        
    def runTrade(self, trader):
        if trader is None : 
            raise ValueError("trader is none.")
        
        #datatable copy 
        self.resultData = self.data.copy()
        
        print("start to run algorithm---")
        
        trader.initialize()
        
        iCapital = trader.getInitialCapital()
        iComm    = trader.getCommission()
        iAmount  = 0
        
        self.resultData["current"]  = 0    
        self.resultData["after"]= 0
        self.resultData["deal"]= 0
        self.resultData["orderamount"]= 0
        self.resultData["profit"]= 0.0
        self.resultData["asset"]= 0.0
        self.resultData["assetprofit"]= 0.0
       
        for index, row in self.resultData.iterrows():
            
            tItem = trader.TradeItem(
                    date = index ,
                    open_price = row["open"],
                    close_price = row["close"],
                    min_price = row["high"],
                    max_price = row["low"],
                    volume = row["volume"],
                    predict_open_price = row["predict_open"],
                    predict_price = row["predict"],
                    current_capital = iCapital,
                    my_amount = iAmount
            )
            
            trader.handle_data(tItem)
            
            ##commission logic add 
            iCapital = tItem.after_capital
            iAmount  = tItem.my_amount
            
            tItem.open_asset = tItem.after_capital + (tItem.open_price * tItem.my_amount)
            tItem.close_asset = tItem.after_capital + (tItem.close_price * tItem.my_amount)
            tItem.profit_rate = float((tItem.after_capital - trader.getInitialCapital())) / float(trader.getInitialCapital())
            tItem.asset_open_profit_rate = float((tItem.open_asset - trader.getInitialCapital())) / float(trader.getInitialCapital())
            tItem.asset_close_profit_rate = float((tItem.close_asset - trader.getInitialCapital())) / float(trader.getInitialCapital())
            
            self.resultData.set_value(index,"current_capital",tItem.current_capital)
            self.resultData.set_value(index,"after_capital",tItem.after_capital)
            self.resultData.set_value(index,"deal",tItem.deal)
            self.resultData.set_value(index,"order_amount",tItem.order_amount)
            self.resultData.set_value(index,"act_amount",tItem.act_amount)
            self.resultData.set_value(index,"my_amount",tItem.my_amount)
            self.resultData.set_value(index,"profit_rate",tItem.profit_rate)
            self.resultData.set_value(index,"open_asset",tItem.open_asset)
            self.resultData.set_value(index,"close_asset",tItem.close_asset)
            self.resultData.set_value(index,"asset_open_profit_rate",tItem.asset_open_profit_rate)
            self.resultData.set_value(index,"asset_close_profit_rate",tItem.asset_close_profit_rate)
            
            trader.appendItem(tItem)
            
        print("end to run algorithm---")
       
