import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from statsmodels.tsa.arima_model import ARIMA
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
from sklearn.metrics import explained_variance_score, mean_squared_error, mean_absolute_error, r2_score
from math import sqrt

class Predictor:
    def __init__(self):
        pass

    @staticmethod
    def predict(data):
        print("start predict ...test")
        #arima + macd
        stepSize = 2
        windowSize = 180
        predicts = []
        predicts1 = []
        sr = data['MACD_D']

        for i in range(len(sr)):
            if i < windowSize:
                predicts.append(0)
                predicts1.append(0)
                continue

            subSr = sr[i - windowSize + 1:i + 1].dropna()
            train = [x for x in subSr]
            model = ARIMA(train, order=(2, 1, 0))
            model_fit = model.fit(disp=False, trend="nc")
            output = model_fit.forecast(steps=stepSize)
            predicts.append(output[0][0])
            predicts1.append(output[0][1])

        data['pre_MACD_D'] = pd.Series(predicts, index=data.index)
        data['pre_MACD_D_1'] = data["pre_MACD_D"].shift(1)
        data['pre_MACD_D2'] = pd.Series(predicts1, index=data.index)
        data['pre_MACD_D2_1'] = data["pre_MACD_D2"].shift(1)

        print("end predict ...")
        return data
        '''
        #test code
        sr = data['MACD_D'].dropna()
        size = int(len(sr) * 0.66)
        stepSize = 2
        windowSize = 60
        train, test = sr[0:size], sr[size:len(sr)]
        history = [x for x in train]
        predictions = list()
        for t in range(len(test)):
            if t % stepSize == 0:
                size = min(stepSize, len(test) - t)
                model = ARIMA(history[windowSize:], order=(2, 1, 0))
                model_fit = model.fit(disp=False, trend="nc")
                output = model_fit.forecast(steps=size)
                yh = output[0]
                #predictions.append(yh)
                predictions.extend(yh)
            obs = test[t]
            history.append(obs)
            #print('predicted=%f, expected=%f, diff=%f' % (yh[t % stepSize], obs, yh[t % stepSize] - obs))

        error = mean_squared_error(test, predictions)

        predictionMv = pd.Series(predictions).rolling(window=2).mean().dropna()
        mvtest = test[len(test) - len(predictionMv):]


        #print('explained_variance_score: {}'.format(explained_variance_score(test, predictions)))
        print('mean_squared_errors: {}'.format(mean_squared_error(test, predictions)))
        print('root mean_squared_errors: {}'.format(sqrt(mean_squared_error(test, predictions))))
        #print('r2_score: {}'.format(r2_score(test, predictions)))

        plt.plot(test)
        plt.plot(predictions, color='red')
        plt.plot(predictionMv, color='green')
        plt.show()
        '''
'''
solvers = ['lbfgs', 'bfgs', 'newton', 'nm', 'cg', 'ncg', 'powell']
model_fit = model.fit(disp=False, solver=solver)
'''
