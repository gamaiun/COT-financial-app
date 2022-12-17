# Import Libraries

import streamlit as st
import pandas as pd
from pandas_profiling import ProfileReport
from streamlit_pandas_profiling import st_profile_report
import sys, os 
import requests
import datetime
#import pandas_datareader.data as web
import yfinance as yf
import matplotlib.pyplot as plt

import plotly.offline as pyo
from plotly.subplots import make_subplots

import os

#plt.style.use("seaborn")

import dash 
from dash import Dash, dcc, html, Input, Output
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
from dash_bootstrap_components._components.Container import Container
import plotly.express as px
import altair as alt
import matplotlib.pyplot as plt
import plotly.graph_objects as go


# Sidebar
st.set_page_config(layout="wide")

df = pd.read_csv('cots2.csv')
forex = pd.read_csv("forex.csv")

df_copy = df.copy()
forex_copy = forex.copy()
forex_copy.reset_index()

st.markdown("""
        <style>
               .css-18e3th9 {
                    padding-top: 0rem;
                    padding-bottom: 0rem;
                    padding-left: 5rem;
                    padding-right: 5rem;
                }
               .css-1d391kg {
                    padding-top: 0rem;
                    padding-right: 1rem;
                    padding-bottom: 0rem;
                    padding-left: 1rem;
                }
        </style>
        """, unsafe_allow_html=True)


#################### Sidebar ######################
today = datetime.date.today()
with st.sidebar:
 #   st.write("---")
    forex_pair = st.sidebar.selectbox("FOREX PAIR", ('GBP|USD', 
                                        'NZD|USD',
                                        'USD|CHF',
                                        "USD|CAD",
                                        "AUD|USD",
                                        "JPY|USD"))

    MA = st.number_input("MOVING AVERAGE", min_value = 0, value = 50)
    start_date = st.date_input(label = "FROM", value=pd.to_datetime("2015-01-31", format="%Y-%m-%d"))
    end_date = st.date_input(label = "TO", value = today)
    cot_instrument = st.sidebar.selectbox("COT INSTRUMENT",("Japanese Yen", 
                                                    "US Dollar", 
                                                    "British Pound", 
                                                    "New Zealand Dollar",
                                                    "Australian Dollar", 
                                                    "Canadian Dollar", 
                                                   "Swiss Frank" ))
    cot_report = st.sidebar.selectbox("COT REPORT",(df_copy.columns[1:17] ))
    cot_indicator = st.sidebar.selectbox("COT INDICATOR",(df_copy.columns[19:] ))


############## Forex Chart ################

forex_coin = forex_copy[forex_copy.coin == forex_pair]

#fig2 = px.line(forex_coin, x = "Date", y = "Close", title = forex_pair, width=1200) 

fig = go.Figure([go.Scatter(x=forex_coin["Date"], y = forex_coin["Close"], line = dict(color='black', width=1), name = " ")])

fig.add_trace(go.Scatter(x= forex_coin["Date"], y=forex_coin.Close.rolling(MA).mean(),
                          line = dict(color='firebrick', width=1)))
fig.update_xaxes(range=[start_date, end_date])
fig.update_layout(go.Layout(margin=dict(t=0), height=300),showlegend=False )
fig.add_annotation(text=f"{forex_pair} vs {MA} Moving Avg.",
                  xref="paper", yref="paper",
                  x=0.010, y=0.85, showarrow=False)

with st.container():
    st.plotly_chart(fig, height = 150, width = 100, use_container_width=True)


###################### COT Report Chart ########################

cot_coin = df_copy[df_copy.coin == cot_instrument]


fig2 = go.Figure([go.Scatter(x=cot_coin["Date"], y = cot_coin[cot_report], line = dict(color='black', width=1))])

fig2.add_trace(go.Scatter(x= cot_coin["Date"], y=cot_coin[cot_report].rolling(MA).mean(), name=f'{MA}-MA',
                           line = dict(color='firebrick', width=1)))
fig2.update_xaxes(range=[start_date, end_date])
fig2.update_layout(go.Layout(margin=dict(t=0),  height=260), showlegend=False)

fig2.add_annotation(text=f"{cot_report} COT report of {cot_instrument}.",
                  xref="paper", yref="paper",
                  x=0.010, y=0.95, showarrow=False)

with st.container():
     st.plotly_chart(fig2, width = 1000, use_container_width=True)

###################### INDICATOR ####################
#cot_indicator = cot_coin[df_copy.coin == cot_instrument]


fig3 = go.Figure([go.Scatter(x=cot_coin["Date"], y = cot_coin[cot_indicator], line = dict(color='black', width=1))])

fig3.add_trace(go.Scatter(x= cot_coin["Date"], y=cot_coin[cot_indicator].rolling(MA).mean(), name=f'{MA}-MA',
                           line = dict(color='firebrick', width=1)))
fig3.update_xaxes(range=[start_date, end_date])
fig3.update_layout(go.Layout(margin=dict(t=0),  height=260), showlegend=False)
    
fig3.add_annotation(text=f"{cot_indicator} COT report of {cot_instrument}.",
                  xref="paper", yref="paper",
                  x=0.010, y=0.95, showarrow=False)

with st.container():
     st.plotly_chart(fig3, width = 1000, use_container_width=True)
