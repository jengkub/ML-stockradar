import numpy as np
import pandas as pd
from datetime import timedelta, datetime
import yfinance as yf
import plotly.graph_objs as go
import csv

class stock:
    def __init__(self,Company):
        self.Company = Company
    
    def saveData(self,Date):
        df_list = list()
        for ticker in self.Company:
            data = yf.download(tickers=ticker, period=Date , interval='1h')
            data['ticker'] = ticker
            df_list.append(data)

        df = pd.concat(df_list)
        df.to_csv('data.csv')

    def info(self,ticker):
        data = yf.Ticker(ticker)
        print(data.info)

    

