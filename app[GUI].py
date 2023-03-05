# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

from dash import Dash, html, dcc
import plotly.express as px
import pandas as pd

import numpy as np
import pandas as pd
import plotly

#Data Source
import yfinance as yf

#Data viz
import plotly.graph_objs as go
import sqlite3

app = Dash(__name__)

# assume you have a "long-form" data frame
# see https://plotly.com/python/px-arguments/ for more options


conn = sqlite3.connect("stock.sqlite")
cur = conn.cursor()
# ticker = input("Enter tickers")
ticker = 'AAV.BK'
query1 = "select * from stock_table_hr where `ticker` == '%s' and datetime > '2023-01-01' and datetime < '2023-01-06'" % ticker
query2 = "select * from stock_table_d where `ticker` == '%s' and datetime > '2022-05-01' and datetime < '2023-01-06'" % ticker
query3 = "select * from stock_table_mo where `ticker` == '%s' and datetime > '2022-01-05' and datetime < '2023-01-06'" % ticker
Hr = pd.read_sql(query1,conn)
Day = pd.read_sql(query2,conn)
Mo = pd.read_sql(query3,conn)
#declare figure
fig = go.Figure()
# Day['time'] = pd.to_datetime(Day['Datetime'])
# Day.set_index(Day['time'],inplace = True)

#Candlestick
for column in [Hr,Day,Mo]:
    # name = column.Ticker[0]
    column['time'] = pd.to_datetime(column['Datetime'])
    column['MA50'] = column['Close'].rolling(window = 50 , min_periods = 0).mean()
    column['MA200'] = column['Close'].rolling(window = 200 , min_periods = 0).mean()
    column.set_index(column['time'],inplace = True)
    fig.add_trace(go.Candlestick(x=column.Datetime,
                    open=column.Open,
                    high=column.High,
                    low=column.Low,
                    close=column.Close, 
                    name = ticker,))
    fig.add_trace(go.Scatter(name = 'MA50',x=column.Datetime,y=column['MA50']))
    fig.add_trace(go.Scatter(name = 'MA200',x=column.Datetime,y=column['MA200']))
    
    
df_resample_hr = Hr.resample('H').max()
merged_index_hr  = Hr.index.append(df_resample_hr.index)
timegap_hr = merged_index_hr[~merged_index_hr.duplicated(keep = False)]

df_resample_day = Day.resample('D').max()
merged_index_day  = Day.index.append(df_resample_day.index)
timegap_day = merged_index_day[~merged_index_day.duplicated(keep = False)]

# fig.update_xaxes( rangebreaks=[ dict(values = timegap_hr , dvalue = 3600000)])

fig.update_xaxes(rangebreaks=[dict(values=timegap_day),
                              dict(values=timegap_hr, dvalue=3600000)])

fig.update_layout(
    updatemenus=[go.layout.Updatemenu(
        active=0,
        buttons=list(
            [dict(label = 'Disable',
                method = 'update',
                args = [{'visible': [False, False, False]}, # the index of True aligns with the indices of plot traces
                        {'title': 'Disable',
                        'showlegend':True}]),
            dict(label = 'Hour',
                method = 'update',
                args = [{'visible': [True, True, True, False, False, False, False, False, False]},
                        {'title': '%s Hour' % ticker,
                        'showlegend':True}]),
            dict(label = 'Day',
                method = 'update',
                args = [{'visible': [False, False, False, True, True, True, False, False, False]},
                        {'title': '%s Day' % ticker,
                        'showlegend':True}]),
            dict(label = 'Mount',
                method = 'update',
                args = [{'visible': [False, False, False, False, False, False, True, True, True]},
                        {'title': '%s Mount' % ticker,
                        'showlegend':True}]),
            ])
        )
    ])
# fig.update_yaxes(rangemode="nonnegative")
# fig.update_xaxes(rangemode="nonnegative")
fig.update_traces(visible="legendonly")
fig.update_yaxes(fixedrange=False)
fig.update_layout(hovermode = "x")
# fig.update_xaxes(
#         rangeslider_visible=True,
#         rangebreaks=[
#             # NOTE: Below values are bound (not single values), ie. hide x to y
#             dict(bounds=["sat", "mon"]),  # hide weekends, eg. hide sat to before mon
#             dict(bounds=[16, 9.5], pattern="hour"),  # hide hours outside of 9.30am-4pm
#             # dict(values=["2019-12-25", "2020-12-24"])  # hide holidays (Christmas and New Year's, etc)
#         ]
#     )

# X-Axes
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

#Show


app.layout = html.Div(children=[
    html.H1(children='Hello Dash'),

    html.Div(children='''
        Dash: A web application framework for your data.
    '''),

    dcc.Graph(
        id='example-graph',
        figure=fig
    )
])

if __name__ == '__main__':
    app.run_server(debug=True)