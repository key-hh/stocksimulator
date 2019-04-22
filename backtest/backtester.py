'''
Created on 2017. 2. 14.

@author: Administrator
'''
from trader import TradeItem


#backtesting manager
class BackTest:
    def __init__(self):
        pass
    
    def run_trade(self, trader, data):
        try:
            if trader is None:
                raise ValueError("trader is none.")
            if data is None:
                raise ValueError("data is none.")

            print("start to trade ---")

            # datatable copy
            resultdata = data.copy()

            trader.initialize()

            capital = trader.get_initial_capital()
            amount = 0

            resultdata["current"] = 0
            resultdata["after"] = 0
            resultdata["deal"] = 0
            resultdata["orderamount"] = 0
            resultdata["profit"] = 0.0
            resultdata["asset"] = 0.0
            resultdata["assetprofit"] = 0.0

            exceptField = ["datetime", "open", "close"]

            for index, row in resultdata.iterrows():
                tItem = TradeItem(
                    date=index,
                    open_price=row["open"],
                    close_price=row["close"],
                    data=row,
                    current_capital=capital,
                    my_amount=amount
                )
                trader.handle_data(tItem)

                # commission logic add
                capital = tItem.after_capital
                amount = tItem.my_amount

                tItem.open_asset = tItem.after_capital + (tItem.open_price * tItem.my_amount)
                tItem.close_asset = tItem.after_capital + (tItem.close_price * tItem.my_amount)
                tItem.profit_rate = float((tItem.after_capital - trader.get_initial_capital())) / float(
                    trader.get_initial_capital())
                tItem.asset_open_profit_rate = float((tItem.open_asset - trader.get_initial_capital())) / float(
                    trader.get_initial_capital())
                tItem.asset_close_profit_rate = float((tItem.close_asset - trader.get_initial_capital())) / float(
                    trader.get_initial_capital())

                for attr, value in tItem.__dict__.iteritems():
                    if attr not in exceptField:
                        resultdata[attr] = value
                '''
                resultdata.set_value(index, "current_capital", tItem.current_capital)
                resultdata.set_value(index, "after_capital", tItem.after_capital)
                resultdata.set_value(index, "deal", tItem.deal)
                resultdata.set_value(index, "order_amount", tItem.order_amount)
                resultdata.set_value(index, "act_amount", tItem.act_amount)
                resultdata.set_value(index, "my_amount", tItem.my_amount)
                resultdata.set_value(index, "profit_rate", tItem.profit_rate)
                resultdata.set_value(index, "open_asset", tItem.open_asset)
                resultdata.set_value(index, "close_asset", tItem.close_asset)
                resultdata.set_value(index, "asset_open_profit_rate", tItem.asset_open_profit_rate)
                resultdata.set_value(index, "asset_close_profit_rate", tItem.asset_close_profit_rate)
'''
                trader.append_trade_item(tItem)
                trader.increase_index()

            print("end to trade ---")

            return resultdata

        except Exception as e:
            print("trader error:", str(e))
            raise