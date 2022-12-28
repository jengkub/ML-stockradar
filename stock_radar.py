import numpy as np
import pandas as pd
import yfinance as yf
import plotly.graph_objs as go
import unittest
from unittest.mock import patch, mock_open
import csv
import datetime

class StockTestcase(unittest.TestCase):
    # def testSave(self):
    #     pass

    def testLastDate(self):
        ticker = 'NKE'
        a = '''2022-12-27 09:30:00,116.47000122070312,117.55000305175781,115.81999969482422,117.30999755859375,117.30999755859375,1100997,NKE
2022-12-27 10:30:00,117.31500244140625,118.0,117.31500244140625,117.81999969482422,117.81999969482422,1070766,NKE
2022-12-27 11:30:00,117.80999755859375,118.19830322265625,117.66999816894531,118.02999877929688,118.02999877929688,654152,NKE
2022-12-27 12:30:00,118.04499816894531,118.19000244140625,117.66999816894531,117.70999908447266,117.70999908447266,456846,NKE
2022-12-27 13:30:00,117.7300033569336,117.7300033569336,117.29000091552734,117.3499984741211,117.3499984741211,600327,NKE
2022-12-27 14:30:00,117.35590362548828,117.58000183105469,117.19499969482422,117.55999755859375,117.55999755859375,1042972,NKE
2022-12-27 15:30:00,117.55999755859375,117.70999908447266,117.4000015258789,117.55999755859375,117.55999755859375,986334,NKE
2022-12-28 09:30:00,117.58000183105469,118.23999786376953,116.48999786376953,116.5999984741211,116.5999984741211,1342269,NKE
2022-12-28 10:30:00,116.5999984741211,116.80000305175781,116.08999633789062,116.2699966430664,116.2699966430664,720219,NKE
2022-12-28 11:30:00,116.28500366210938,116.36000061035156,115.33000183105469,115.5999984741211,115.5999984741211,599413,NKE
2022-12-28 12:30:00,115.61000061035156,116.32589721679688,115.5999984741211,116.26000213623047,116.26000213623047,275603,NKE'''
        tester = ML_stock(ticker)
        with patch("builtins.open", mock_open(read_data= a)) as mock_file:
            result = tester.getLastDate("path/to/open",ticker)
            assert result == ['2022', '12', '28']

#     def testUpdate(self):
#         ticker = 'NKE'
#         a = '''2022-12-27 09:30:00,116.47000122070312,117.55000305175781,115.81999969482422,117.30999755859375,117.30999755859375,1100997,NKE
# 2022-12-27 10:30:00,117.31500244140625,118.0,117.31500244140625,117.81999969482422,117.81999969482422,1070766,NKE
# 2022-12-27 11:30:00,117.80999755859375,118.19830322265625,117.66999816894531,118.02999877929688,118.02999877929688,654152,NKE
# 2022-12-27 12:30:00,118.04499816894531,118.19000244140625,117.66999816894531,117.70999908447266,117.70999908447266,456846,NKE
# 2022-12-27 13:30:00,117.7300033569336,117.7300033569336,117.29000091552734,117.3499984741211,117.3499984741211,600327,NKE
# 2022-12-27 14:30:00,117.35590362548828,117.58000183105469,117.19499969482422,117.55999755859375,117.55999755859375,1042972,NKE
# 2022-12-27 15:30:00,117.55999755859375,117.70999908447266,117.4000015258789,117.55999755859375,117.55999755859375,986334,NKE
# 2022-12-28 09:30:00,117.58000183105469,118.23999786376953,116.48999786376953,116.5999984741211,116.5999984741211,1342269,NKE
# 2022-12-28 10:30:00,116.5999984741211,116.80000305175781,116.08999633789062,116.2699966430664,116.2699966430664,720219,NKE
# 2022-12-28 11:30:00,116.28500366210938,116.36000061035156,115.33000183105469,115.5999984741211,115.5999984741211,599413,NKE
# 2022-12-28 12:30:00,115.61000061035156,116.32589721679688,115.5999984741211,116.26000213623047,116.26000213623047,275603,NKE'''
#         tester = ML_stock(ticker)
#         with patch("builtins.open", mock_open(read_data= a)) as mock_file:
#             tester.getLastDate("path/to/open",ticker)
#             tester.getDiffDay()
#             tester.update('path/to/open',ticker)
#             result = tester.getDiffDay()
#             assert result == 1

class ML_stock:
    def __init__(self,Company):
        self.last = []
        self.LastDate = []
        self.DiffDay = 0
        self.Company = Company
    
    def saveData(self,Date):
        df_list = list()
        for ticker in self.Company:
            data = yf.download(tickers=ticker, period=Date , interval='1h')
            data['ticker'] = ticker
            df_list.append(data)
        df = pd.concat(df_list)
        df.to_csv('data.csv')

    def info(self):
        data = yf.Ticker(self.Company)
        return data.info

    def getLastDate(self,name,ticker):
        with open(name,'r') as file:
            reader = csv.reader(file)
            for row in reader:
                if row[7] == ticker:
                    self.last = row
        
        self.LastDate = self.last[0].split()[0].split('-')
        return self.LastDate

    def getDiffDay(self):
        x = datetime.datetime.now()
        DayMo365 = {'1':31,'2':28,'3':31,'4':30,'5':31,'6':30,'7':31,'8':31,'9':30,'10':31,'11':30,'12':31}
        DiffMo = int(x.month) - int(self.LastDate[1])
        DiffYe = int(x.year) - int(self.LastDate[0])
        if DiffYe == 0:
            if DiffMo == 0:
                DiffDay = int(x.day) - int(self.LastDate[2])
                if DiffDay != 0:
                    self.DiffDay = str(DiffDay) + 'd'
            elif DiffMo != 0 :
                for u in range(DiffMo):
                    DayM = DayM + DayMo365[str(int(self.LastDate[1])+count)]
                    count += 1
                DiffDay = DayM - int(self.LastDate[2]) + int(x.day)
                self.DiffDay = str(DiffDay) + 'd'
        elif DiffYe != 0:
            dayly = 0
            dayn = 0
            for j in range(1,int(self.LastDate[1])):
                dayly = dayly + DayMo365[str(j)]
            for i in range(1,int(x.month)):
                dayn = dayn + DayMo365[str(i)]
            DiffDay = (365*DiffYe) - dayly + dayn - int(self.LastDate[2]) + int(x.day)
            self.DiffDay = str(DiffDay) + 'd'
        return DiffDay
        
    def update(self,name,ticker):
        data = yf.download(tickers=ticker, period=self.DiffDay, interval='1h')
        count = 0
        for i in data.index.day:
            if data.index.year[count] == int(self.LastDate[0]):
                if data.index.month[count] == int(self.LastDate[1]):
                    if i == int(self.LastDate[2])+1:
                        break
            count += 1

        data['ticker'] = 'NKE'
        data = data.iloc[count:,:]
        data
        data.to_csv(name,mode='a',header=False)

    def plot(self):
        data = yf.download(tickers=self.Company, period='1d', interval='1m')
        fig = go.Figure()
        fig.add_trace(go.Candlestick(x=data.index,
                        open=data['Open'],
                        high=data['High'],
                        low=data['Low'],
                        close=data['Close'], name = 'market data'))

        fig.update_layout(
            title=self.Company,
            yaxis_title='Stock Price (USD per Shares)')

        fig.update_xaxes(
            rangeslider_visible=True,
            rangeselector=dict(
                buttons=list([
                    dict(count=15, label="15m", step="minute", stepmode="backward"),
                    dict(count=45, label="45m", step="minute", stepmode="backward"),
                    dict(count=1, label="HTD", step="hour", stepmode="todate"),
                    dict(count=3, label="3h", step="hour", stepmode="backward"),
                    dict(step="all")
                ])
            )
        )

        fig.show()

    
# if __name__ == '__main__':
#     unittest.main()
ticker = 'NKE'
a = ML_stock(ticker)
a.getLastDate('test.csv',ticker)
print(a.getDiffDay())
a.update('test.csv',ticker)