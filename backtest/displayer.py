'''
Created on 2017. 2. 14.
display method 
@author: Administrator
'''

import matplotlib.pyplot as plt
from datetime import datetime

class ConsoleDisplayer:
    def display(self, data):
        print(data.tail(10))
    def displayResult(self, data, rdata):
        print(rdata.tail(10))
    
class PlotDisplayer:
    def display(self, data):
        plt.plot(data)
    def displayResult(self, data, rdata):
        plt.plot(rdata)

class ExcelDisplayer:
    def display(self, data):
        data.to_csv("C:\\Data_" +datetime.now().strftime("%Y%m%d%H%M%S")+ ".csv")
    def displayResult(self, data, rdata):
        rdata.to_csv("C:\\resultData_" +datetime.now().strftime("%Y%m%d%H%M%S")+ ".csv")
    