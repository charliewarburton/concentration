# Stock Concentration in S&P 500
# Install packages
import pandas as pd
import numpy as np
import streamlit as st
import yfinance as yf

st.title('S&P 500 Stock Concentration Calculator')

n_stocks = st.sidebar.number_input("Enter the number of top stocks to calculate concentration for:", min_value=1, max_value=500, value=5)

# Function to get the market cap of a given ticker
def get_market_cap(ticker):
    stock = yf.Ticker(ticker)
    return stock.info['marketCap']

# Fetch S&P 500 tickers from Wikipedia - has to be done this way
# st.cache stores results of function calls for quick access when script is rerun (user interacts with app)
@st.cache_data
def get_sp500_tickers():
    sp500_url = 'https://en.wikipedia.org/wiki/List_of_S%26P_500_companies'
    sp500_table = pd.read_html(sp500_url)
    sp500_df = sp500_table[0]
    return sp500_df['Symbol'].tolist()

sp500_tickers = get_sp500_tickers()


 
# Get market caps for all S&P 500 components
@st.cache_data
def get_market_caps(tickers):
    market_caps = {}
    for ticker in tickers:
        try:
            market_caps[ticker] = get_market_cap(ticker)
        except KeyError:
            market_caps[ticker] = 0
    return market_caps
    
# Returns dictionary of Ticker: Market Cap
market_caps = get_market_caps(sp500_tickers)
# Transform dictionary into df for easier wrangling
market_caps_df = pd.DataFrame(list(market_caps.items()), columns=["Ticker", "MarketCap"])


# Calculate total market cap of the S&P 500
total_market_cap = market_caps_df['MarketCap'].sum()

# Get the top n companies by market cap
top_n = market_caps_df.sort_values(by='MarketCap', ascending=False).head(n_stocks)
top_n_market_cap = top_n['MarketCap'].sum()

concentration = top_n_market_cap/total_market_cap *100

st.write(f"The concentration of the top {n_stocks} stocks in the S&P 500 is {concentration:.2f}%")

