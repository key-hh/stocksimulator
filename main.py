from crawl.crawler import *
from analyzer.indexer import *
from backtest import *
import matplotlib.pyplot as plt

# code
# reverage: 122639
# inverse:252670


# trade algorithm
class TestTrader(trader.Trade):
    def initialize(self):
        self.set_initial_capital(1000000)
        self.set_commission(0)

        # self variable
        self.deadlinePrice = -200000

    def handle_data(self, item):
        # data : current data
        # amount: greater than 0: sell , less than 0 : buy

        if self.get_index() > 5:
            # 3days history
            thrdaysHistory = self.history(4)

            openprice = item.open_price
            closeprice = item.close_price
            sec = thrdaysHistory[-2].close_price  # 2day before
            frc = thrdaysHistory[-3].close_price  # 1day before
            seo = thrdaysHistory[-2].open_price  # 2day before
            fro = thrdaysHistory[-3].open_price  # 1day before

            orderAmount = -1

            self.order(item, orderAmount, trader.TradeDiv.CLOSE_BASE)


if __name__ == "__main__":
    codeList = [252670]
    for code in codeList:
        try:
            # get price data
            data = Crawler.get_price(code, 50)

            # make index data
            data = Index.make_index(data, IndexRequest())

            # trade
            bt = backtester.BackTest()
            result = bt.run_trade(TestTrader(), data)

            displayer.ConsoleDisplayer.display(result)
        except Exception as e:
            print(str(e))
            raise