import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.graph_objects as go
sns.set()


#yfinance API used to generate real time stock data
import yfinance as yf

#suppress warnings from libraries
import warnings 
warnings.filterwarnings("ignore")

st.set_page_config(layout='wide')

#Create a sidebar
st.sidebar.title("Navigation")
sections = ['Domain Knowledge','Data Extraction','Data Preview',
            'Data Summary', 'Data Visualization', 'Feature Engineering', 'Conclusion', 'Downloads']
page = st.sidebar.radio("Select a section:", sections)

st.title("Stock Prices Dashboard")

st.write("Author: Siya Msiza")

if page == 'Domain Knowledge':
    st.header("Domain Knowledge")
    st.subheader("Background Information")
    st.write("A company's stock represents a portion of ownership in the company. More specifically, a stock (also referred to as equity) is a security that signifies partial ownership in a corporation, granting the shareholder a claim to a portion of the corporation's assets and profits proportional to the number of shares owned. Shares are individual units of stock.")
    st.write("Investors can buy stocks and later sell them. If the stock price rises, the investor makes a profit; if it falls, the investor incurs a loss. Stock prices are influenced by numerous factors, including the number of outstanding shares and the company’s projected future profits, making price determination complex. Stocks are traded continuously throughout the day, and the stock ticker is an ongoing report of the price of specific stocks, updated in real-time by various stock exchanges.")
    
    
if page == 'Data Extraction':
   st.subheader("Data Extraction")
   st.write('Use Yahoo finance API To Extract Stock Data of Your Choice. Choose from the range of corporations.')
   # Create a dictionary of companies and their ticker symbols
   data = {
    'Company': ['Apple Inc', 'Tesla, Inc', 'Microsoft Corporation', 'Amazon.com, Inc',
                'Alphabet Inc. (Google)', 'Meta Platforms, Inc. (formerly Facebook)',
                'Netflix, Inc.', 'NVIDIA Corporation', 'Berkshire Hathaway Inc. (Class A)',
                'JP Morgan Chase & Co.'],
    'Ticker Symbol': ['AAPL', 'TSLA', 'MSFT', 'AMZN', 'GOOGL', 'META', 'NFLX', 'NVDA', 'BRK-A', 'JPM']
}

# Convert the dictionary to a DataFrame
   df = pd.DataFrame(data)

# Display the DataFrame as a table in Streamlit
   st.write("### Company Ticker Symbols")
   st.table(df)
   tickers = ['AAPL','TSLA','MSFT','AMZN','GOOGL','META','NFLX','NVDA','BRK-A','JPM']
   selected_ticker = st.selectbox("Select the company you want stock data for:", tickers)

   ticker = yf.Ticker(selected_ticker)

   ticker_data = ticker.history(period='max')

   # In 'Data Extraction' Section
   st.write("Select the time period for stock data extraction:")
   start_date = st.date_input("Start Date", pd.to_datetime("2010-01-01"))
   end_date = st.date_input("End Date", pd.to_datetime("today"))

   ticker_data = ticker.history(start=start_date, end=end_date)
   ticker_data.reset_index(inplace=True)

   st.session_state['ticker_data'] = ticker_data
   st.session_state['selected_ticker'] = selected_ticker
   st.success(f"{selected_ticker} stock data has been succefully extracted.")


if 'ticker_data' in st.session_state:
    ticker_data = st.session_state['ticker_data']
    selected_ticker = st.session_state['selected_ticker']

    if page=="Data Preview":
        st.subheader("Data Preview")
        st.write(f"5 {selected_ticker} latest stock data updates:")
        st.write(ticker_data.tail())
        st.write(f"Number of Rows: {ticker_data.shape[0]}")
        st.write(f"Number of Columns: {ticker_data.shape[1]}")
        if any(ticker_data.isnull().sum()) == False:
            st.write("There are no missing values in this dataset.")
        else:
            st.write(f"There are {ticker_data.isnull().count()} missing values in total.")

    if page=="Data Summary":
        st.subheader("Data Summary")
        st.write(ticker_data.describe())
        st.write("#### Best & Worst Days")

        #Daily returns
        ticker_data['Daily Return'] = ticker_data['Close'].pct_change()
    
        # Best and worst days based on percentage change
        best_day = ticker_data.loc[ticker_data['Daily Return'].idxmax()]
        worst_day = ticker_data.loc[ticker_data['Daily Return'].idxmin()]
    
        st.write(f"**Best Day**: {best_day['Date'].strftime('%Y-%m-%d')} with a return of {best_day['Daily Return']*100:.2f}%")
        st.write(f"**Worst Day**: {worst_day['Date'].strftime('%Y-%m-%d')} with a return of {worst_day['Daily Return']*100:.2f}%")

        df_num = ticker_data.drop(['Date','Dividends', 'Stock Splits', 'Volume'], axis=1)
        st.subheader(f"Daily Return Price Distribution")
        
        fig1 = go.Figure(data=[go.Histogram(x=df_num['Daily Return'], nbinsx=20)])
        fig1.update_layout(title=f"Daily Return Price Distribution for {selected_ticker}",
                               xaxis_title=f"Daily Return (USD)",
                               yaxis_title="Count")
        st.plotly_chart(fig1)


    if page == "Data Visualization":
        st.subheader("Data Visualization")

        # Use Plotly for an interactive graph
        st.write("### Interactive Stock Price Chart")
        fig_plotly = go.Figure([go.Scatter(x=ticker_data['Date'], y=ticker_data['Close'], mode='lines', name='Close Price')])
        fig_plotly.update_layout(title=f'{selected_ticker} Stock Price Over Time',
                                 xaxis_title='Year',
                                 yaxis_title='Close Price (USD)')
        st.plotly_chart(fig_plotly)

      
        st.write("### Interactive Candlestick Chart")
        candlestick = go.Figure(data=[go.Candlestick(x=ticker_data['Date'],
                    open=ticker_data['Open'],
                    high=ticker_data['High'],
                    low=ticker_data['Low'],
                    close=ticker_data['Close'])])
    
        candlestick.update_layout(title=f'{selected_ticker} Candlestick Chart', 
                              xaxis_title='Date', 
                              yaxis_title='Price (USD)')
        st.plotly_chart(candlestick)


        #Line plot for stock closing price
        st.write("### Stock Closing Price Over Time")
        sns.set()
        fig, ax = plt.subplots()
        ax.plot(ticker_data['Date'], ticker_data['Close'], color='blue', label='Close Price')
        ax.set_xlabel('Year')
        ax.set_ylabel('Price (USD)')
        ax.set_title(f'{selected_ticker} Stock Closing Price')
        st.pyplot(fig)

        # Show trading volume
        st.write("### Trading Volume Over Time")
        fig, ax = plt.subplots()
        ax.bar(ticker_data['Date'], ticker_data['Volume'], color='red')
        ax.set_xlabel('Year')
        ax.set_ylabel('Volume')
        ax.set_title(f'{selected_ticker} Trading Volume')
        st.pyplot(fig)

    if page == 'Feature Engineering':
        st.subheader("Feature Engineering")
        # Example feature engineering, like calculating moving averages
        ticker_data['Moving Average (30 days)'] = ticker_data['Close'].rolling(window=30).mean()
        st.write("### Feature: 30-Day Moving Average")
        st.write(ticker_data[['Date', 'Close', 'Moving Average (30 days)']].tail())
        
        # Plot moving average alongside closing price
        st.write("### Closing Price vs 30-Day Moving Average")
        fig, ax = plt.subplots()
        ax.plot(ticker_data['Date'], ticker_data['Close'], color='blue', label='Close Price')
        ax.plot(ticker_data['Date'], ticker_data['Moving Average (30 days)'], color='red', label='30-Day MA')
        ax.set_xlabel('Year')
        ax.set_ylabel('Price (USD)')
        ax.set_title(f'{selected_ticker} Stock Price and Moving Average')
        ax.legend()
        st.pyplot(fig)

        #Correlation matrix
        df_num = ticker_data.drop(['Date', 'Dividends', 'Stock Splits'], axis=1)
        corr_matrix = df_num.corr()
        st.write('### Heatmap: Correlations between Attributes')
        fig, ax = plt.subplots(figsize=(10, 8))
        st.pyplot(fig)        
                
        sns.heatmap(corr_matrix, cmap='coolwarm', annot=True)
        
        
        #performance metrics
        st.subheader("Performance Metrics")
    
        # Calculate ROI
        ticker_data['Daily Return'] = ticker_data['Close'].pct_change()
        ROI = (ticker_data['Close'].iloc[-1] / ticker_data['Close'].iloc[0] - 1) * 100
    
        # Calculate Volatility
        volatility = ticker_data['Daily Return'].std() * np.sqrt(252)

        st.write(f"#### 1. Return on Investment (ROI): {ROI:.2f}%")
        st.write("**Definition**: ROI measures the gain or loss generated on an investment relative to the initial amount invested. It is often expressed as a percentage to quantify how much an investment has grown over a certain period.")


        st.write(f"#### 2. Annualized Volatility: {volatility:.2f}")
        st.write("**Definition**: Volatility measures the degree of variation in the price of a financial asset over time. Annualized Volatility refers to the standard deviation of daily returns, scaled to represent the volatility over a one-year period. It quantifies how much the stock's price tends to fluctuate in a year, reflecting the stock's risk level.")

if page == 'Conclusion':
    st.subheader("Conclusion")
    st.write("The Stock Prices Dashboard provides an insightful and interactive platform for investors and analysts to explore the complexities of stock data. By seamlessly integrating real-time data from Yahoo Finance, users can effortlessly navigate through various sections, gaining valuable knowledge about stock ownership and the factors influencing price movements.")
    st.write("From extracting data on major corporations to visualizing trends through engaging charts, the app empowers users to make informed decisions based on comprehensive analyses. Features like data summaries and feature engineering—such as moving averages and correlation matrices—enhance the understanding of stock behavior, enabling users to uncover patterns that can drive investment strategies.")
    st.write("Whether you are a seasoned investor or just starting your journey in the world of finance, this dashboard serves as a valuable tool to deepen your insights and foster better decision-making in your investment endeavors. Happy investing!")

if page == 'Downloads':
    if 'ticker_data' in st.session_state:
      csv_data = ticker_data.to_csv(index=False)
      st.download_button(
        label="Download Stock Data as CSV",
        data=csv_data,
        file_name=f"{selected_ticker}_stock_data.csv",
        mime='text/csv'
    )

else:
            st.success("Load stock data first in the Data Extraction page!")
