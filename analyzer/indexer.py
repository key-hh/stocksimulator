import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import warnings
from datetime import datetime
import os
import math

class Index:
    def __init__(self):
        pass

    # RSI
    @staticmethod
    def get_rsi(series, period):
        delta = series.diff().dropna()
        u = delta * 0
        d = u.copy()
        u[delta > 0] = delta[delta > 0]
        d[delta < 0] = -delta[delta < 0]
        u[u.index[period - 1]] = np.mean(u[:period])  # first value is sum of avg gains
        u = u.drop(u.index[:(period - 1)])
        d[d.index[period - 1]] = np.mean(d[:period])  # first value is sum of avg losses
        d = d.drop(d.index[:(period - 1)])
        '''
        rs = pd.stats.moments.ewma(u, com=period - 1, adjust=False) / \
             pd.stats.moments.ewma(d, com=period - 1, adjust=False)
        '''
        rs = u.ewm(com=period - 1, adjust=False).mean() / d.ewm(com=period - 1, adjust=False).mean()
        return 100 - 100 / (1 + rs)

    # CCI
    @staticmethod
    def get_cci(data, n):
        TP = (data["close"] + data["high"] + data["low"]) / 3
        CCI = pd.Series((TP - TP.rolling(n).mean()) / (0.015 * TP.rolling(n).std()), name='CCI')
        return CCI

    @staticmethod
    def make_index(data, req):
        try:
            #data["datetime"] = pd.to_datetime(data["datetime"])
            #data = data.set_index("datetime")
            data.sort_index(inplace=True)
            data.insert(len(data.columns), "MA5", data["close"].rolling(window=5).mean())
            data.insert(len(data.columns), "MA10", data["close"].rolling(window=10).mean())
            data.insert(len(data.columns), "MA20", data["close"].rolling(window=20).mean())
            data["close_1"] = data["close"].shift(1)
            data["high_1"] = data["high"].shift(1)
            data["low_1"] = data["low"].shift(1)
            data["diff"] = data["close"] - data["close_1"]

            
            data['RSI'] = Index.get_rsi(data['close'], req.rsiDay)
            data.insert(len(data.columns), "RSI_S", data["RSI"].rolling(window=req.rsiSignal).mean())
            data["RSI_D"] = data["RSI"] - data["RSI_S"]
            data['RSI_1'] = data["RSI"].shift(1)
            data['RSI_S_1'] = data["RSI_S"].shift(1)

            data["CCI"] = Index.get_cci(data, req.cciDay)
            data.insert(len(data.columns), "CCI_S", data["CCI"].rolling(window=req.cciSignal).mean())
            data["CCI_D"] = data["CCI"] - data["CCI_S"]
            data['CCI_1'] = data["CCI"].shift(1)
            data['CCI_S_1'] = data["CCI_S"].shift(1)

            # Stocastic
            tempSto_K = []

            tempDMP = []
            tempDMM = []
            tempTR = []
            sz = len(data['close'])

            for i in range(sz):
                if i >= req.stoDay - 1:
                    tempUp = data['close'][i] - min(data['low'][i - req.stoDay + 1:i + 1])
                    tempDown = max(data['high'][i - req.stoDay + 1:i + 1]) - min(data['low'][i - req.stoDay + 1:i + 1])
                    tempSto_K.append(tempUp / tempDown)
                else:
                    tempSto_K.append(0)

                if i >= req.dmDay - 1:
                    tempd1 = data['high'][i] - data['high_1'][i]
                    tempd2 = data['low_1'][i] - data['low'][i]
                    tempd = data['high'][i] - data['low'][i]
                    if tempd1 > 0 and tempd1 > tempd2:
                        tempDMP.append(tempd1)
                    else:
                        tempDMP.append(0)
                    if tempd2 > 0 and tempd1 < tempd2:
                        tempDMM.append(tempd2)
                    else:
                        tempDMM.append(0)
                    tempTR.append(max([data['high'][i] - data['low'][i], abs(data['close_1'][i] - data['high'][i]),
                                       abs(data['close_1'][i] - data['low'][i])]))
                else:
                    tempDMP.append(0)
                    tempDMM.append(0)
                    tempTR.append(0)
            # Stocastic
            data['sto_K'] = pd.Series(tempSto_K, index=data.index)
            data['sto_D'] = pd.Series(data['sto_K'].rolling(req.stoK).mean())
            data['sto_slowD'] = pd.Series(data['sto_D'].rolling(req.stoD).mean())
            data["STC_D"] = data["sto_D"] - data["sto_slowD"]
            data['sto_D_1'] = data["sto_D"].shift(1)
            data['sto_slowD_1'] = data["sto_slowD"].shift(1)

            # MACD
            data['EMAFast'] = data['close'].ewm(span=req.m_NumFast, min_periods=req.m_NumFast - 1).mean()
            data['EMASlow'] = data['close'].ewm(span=req.m_NumSlow, min_periods=req.m_NumSlow - 1).mean()
            data['MACD'] = data['EMAFast'] - data['EMASlow']
            data['MACDSignal'] = data['MACD'].ewm(span=req.m_NumSignal, min_periods=req.m_NumSignal - 1).mean()
            data['MAC_D'] = data['MACD'] - data['MACDSignal']
            data['MACD_1'] = data["MACD"].shift(1)
            data['MACDSignal_1'] = data["MACDSignal"].shift(1)

            # TRIX
            data['TRX1'] = data['close'].ewm(span=req.trix, min_periods=req.trix - 1).mean()
            data['TRX2'] = data['TRX1'].ewm(span=req.trix, min_periods=req.trix - 1).mean()
            data['TRX3'] = data['TRX2'].ewm(span=req.trix, min_periods=req.trix - 1).mean()
            data['TRX3_1'] = data['TRX3'].shift(1)
            data['TRX'] = (data['TRX3'] - data['TRX3_1']) / data['TRX3_1']
            data['TRXSignal'] = data['TRX'].ewm(span=req.trixSignal, min_periods=req.trixSignal - 1).mean()
            data['TRX_D'] = data["TRX"] - data['TRXSignal']
            data['TRX_1'] = data["TRX"].shift(1)
            data['TRXSignal_1'] = data["TRXSignal"].shift(1)

            # Sonar
            data['SNA_C'] = data['close'].ewm(span=req.s_day, min_periods=req.s_day - 1).mean()
            data['SNA_B'] = data["SNA_C"].shift(req.s_n)
            data['SNA'] = data['SNA_C'] - data['SNA_B']
            data['SNASignal'] = data['SNA'].ewm(span=req.s_signal, min_periods=req.s_signal - 1).mean()
            data['SNA_D'] = data["SNA"] - data['SNASignal']
            data['SNA_1'] = data["SNA"].shift(1)
            data['SNASignal_1'] = data["SNASignal"].shift(1)

            # DMI
            data['DMP'] = pd.Series(tempDMP, index=data.index)
            data['DMM'] = pd.Series(tempDMM, index=data.index)
            data['TR'] = pd.Series(tempTR, index=data.index)
            data['DMPN'] = pd.Series(data['DMP'].rolling(req.dmDay).mean())
            data['DMMN'] = pd.Series(data['DMM'].rolling(req.dmDay).mean())
            data['TRN'] = pd.Series(data['TR'].rolling(req.dmDay).mean())
            data['DLP'] = data['DMPN'] / data['TRN']
            data['DLM'] = data['DMMN'] / data['TRN']
            data['DMI_D'] = data['DLP'] - data['DLM']
            data.drop(["DMP", "DMM", "TR", "DMPN", "DMMN", "TRN"], axis=1, inplace=True)
            data['DLP_1'] = data["DLP"].shift(1)
            data['DLM_1'] = data["DLM"].shift(1)
            return data

        except Exception as e:
            print(str(e))
            raise


class IndexRequest:
    rsiDay = 14
    rsiSignal = 9
    cciDay = 14
    cciSignal = 9
    stoDay = 14
    stoK = 3
    stoD = 3
    dmDay = 9
    m_NumFast = 6
    m_NumSlow = 12
    m_NumSignal = 5
    s_day = 6
    s_n = 12
    s_signal = 10
    trix = 6
    trixSignal = 4