'''
Created on 2017. 2. 14.
display method 
@author: Administrator
'''

import matplotlib.pyplot as plt
from datetime import datetime


class ConsoleDisplayer:
    @staticmethod
    def display(data):
        print(data.tail(10))


class PlotDisplayer:
    @staticmethod
    def display(data):
        plt.plot(data)



