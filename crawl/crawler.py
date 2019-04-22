'''
Created on 2017. 5. 21.

@author: Administrator
'''
import requests
import pandas as pd
from bs4 import BeautifulSoup
import urllib

class Crawler:
    def __init__(self):
        pass
    @staticmethod
    def get_price(code, count):
        try:
            code = (str(code)).zfill(6)
            url = "http://finance.naver.com/item/sise_day.nhn?code=" + code + "&page="
            pageIdx = 1
            datetimeList = []
            closePriceList = []
            startPriceList = []
            minPriceList = []
            maxPriceList = []
            amountList = []

            while pageIdx <= count / 10:
                fullAddr = url + str(pageIdx)
                source_code = requests.get(fullAddr)
                if source_code is None:
                    break
                soup = BeautifulSoup(source_code.text, "lxml")
                for tr in filter(lambda x: x.get("onmouseout") is not None, soup.find_all("tr")):
                    tDate = tr.find("span", class_="tah p10 gray03").text
                    cPrice = tr.find_all("span", class_="tah p11")
                    sIdx = 1
                    if len(cPrice) != 5:
                        sIdx = 2
                    dt = tDate.replace(".", "-")
                    pClose = float(cPrice[0].text.replace(",", ""))
                    pStart = float(cPrice[sIdx].text.replace(",", ""))
                    sIdx += 1
                    pMax = float(cPrice[sIdx].text.replace(",", ""))
                    sIdx += 1
                    pMin = float(cPrice[sIdx].text.replace(",", ""))
                    sIdx += 1
                    amount = float(cPrice[sIdx].text.replace(",", ""))

                    datetimeList.append(dt)
                    closePriceList.append(pClose)
                    startPriceList.append(pStart)
                    minPriceList.append(pMin)
                    maxPriceList.append(pMax)
                    amountList.append(amount)
                pageIdx += 1

            df = pd.DataFrame(
                {"datetime": datetimeList, "close": closePriceList, "open": startPriceList, "low": minPriceList, "high": maxPriceList, "volume": amountList})
            df["datetime"] = df.datetime.map(lambda x: pd.to_datetime(x))
            df = df.set_index("datetime")
            return df
        except Exception as e:
            print(str(e))
            raise

    #not working - page is deprecated
    @staticmethod
    def get_stock_list(div):
        # stype : P - Kospi, Q - Kosdaq
        try:
            base_url = 'http://finance.daum.net/quote/marketvalue.daum?col=listprice&order=desc&stype=' + div + '&page='
            nameList = []
            codeList = []
            for i in range(1, 200):
                url = base_url + str(i)
                source_code = requests.get(url)
                if source_code is None:
                    break
                soup = BeautifulSoup(source_code.text, "lxml")
                tbl = soup.find(id='tabSBody1')
                for tr in tbl.find_all('tr'):
                    td = tr.find_all('td', class_='num cGr left2')
                    if td is None or len(td) == 0:
                        continue
                        break;
                    td = tr.find('td', {"class": "txt"})
                    codeList.append(td.a["href"][-6:])
                    nameList.append(td.a.contents[0])
                # Page Check
                listPaging = soup.find_all('div', class_='listPaging')
                brk = True;
                for a in listPaging[0].descendants:
                    if a.name != 'a':
                        continue
                    if str(i + 1) in a.contents[0]:
                        brk = False
                        break
                if brk:
                    break
            df = pd.DataFrame({"code": codeList, "name": nameList, "div": div})
            return df
        except Exception as e:
            print(str(e))
            raise
