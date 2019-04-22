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
            exceptField = ["datetime", "open_price", "close_price", "data"]

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
                tItem.profit_rate = float((tItem.after_capital - trader.get_initial_capital())) / float(trader.get_initial_capital())
                tItem.asset_open_profit_rate = float((tItem.open_asset - trader.get_initial_capital())) / float(trader.get_initial_capital())
                tItem.asset_close_profit_rate = float((tItem.close_asset - trader.get_initial_capital())) / float(trader.get_initial_capital())
                for attr, value in tItem.__dict__.iteritems():
                    if attr not in exceptField:
                        resultdata.at[index, attr] = value

                trader.append_trade_item(tItem)
                trader.increase_index()

            print("end to trade ---")

            last = resultdata.iloc[-1]
            return resultdata, last["close_asset"], last["asset_close_profit_rate"], resultdata["close_asset"].mean(),

        except Exception as e:
            print("trader error:", str(e))
            raise