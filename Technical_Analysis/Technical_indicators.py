import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import streamlit as st
from talib import abstract
import talib
import ta_py as ta
class TIndicators:
  def __init__(self,data):
    self.df=data
    self.data=data['Close']
    self.techDF =pd.DataFrame() # Technical Indicators Dataframe
    self.sma_50 = 0
    self.sma_200 = 0
    self.rsi = 0
    self.macd = 0
    self.signal = 0
    self.adx = 0

    # State variables
    self.sma_50_greater_than_sma_200 = None
    self.rsi_above_70 = None
    self.macd_above_signal = None
    self.adx_above_25 = None
    self.rsi_below_30 = None
    self.macd_below_signal = None
    self.rsi_below_20 = None

  def MACD(self):
    length1 = 12; # default = 12
    length2 = 26; # default = 26
    length3= 9;
    macd_array = ta.macd(self.data.values, length1, length2)
    signal_line_array = ta.ema(self.data.values,length3)
    # Create a new figure and axis
    fig, ax = plt.subplots()
    # Plot MACD Line and Signal Line on the same axis
    ax.plot(macd_array, label='MACD Line')
    ax.plot(signal_line_array, label='Signal Line')
    # Set axis labels and title
    ax.set_xlabel('Time')
    ax.set_ylabel('Value')
    ax.set_title('MACD and Signal Line')
    # Show legend
    ax.legend()
    # Show the plot
    plt.show()
    st.pyplot(fig)
    return macd_array,signal_line_array
  def BullBearish_state(self):
      # Calculate technical indicators
      if len(self.data)>=250:
        st.title(f"{st.session_state['CurrencyPair']}:chart_with_upwards_trend: :chart_with_downwards_trend: Trend :chart: Strength")
        # Calculate the Simple Moving Average (SMA) with a time period of 50
        self.sma_50 = talib.SMA(self.data, timeperiod=50).tail() # The tail() method returns the last 5 elements of the Series
        # Calculate the Simple Moving Average (SMA) with a time period of 200
        self.sma_200 = talib.SMA(self.data, timeperiod=200).tail()
        # Calculate the Relative Strength Index (RSI)
        self.rsi = talib.RSI(self.data).tail()
        # Calculate the Moving Average Convergence Divergence (MACD) and Signal line
        macd, signal, _ = talib.MACD(self.data)  # Unpack the tuple and remove the third element (histogram)
        self.macd = macd.tail()
        self.signal = signal.tail()
        # Calculate the Average Directional Index (ADX)
        self.adx = talib.ADX(self.df['High'], self.df['Low'], self.data, timeperiod=14).tail()
        @st.cache_data
        # Storing the trend data
        def trendData():
            trendDF=pd.DataFrame()
            trendDF['SMA-50']=self.sma_50
            trendDF['SMA-200']=self.sma_200
            trendDF['RSI']=self.rsi
            trendDF['MACD']=self.macd
            trendDF['Signal']=self.signal
            trendDF['ADX']=self.adx
            trendDF.reset_index(drop=True, inplace=True)
            # Shift the index by adding 1 to each index value to start from 1 instead of 0
            trendDF.index += 1
            return trendDF
        st.header("Table with the 5 recent values")
        st.dataframe(trendData())
        # Splitting each condition into separate boolean variables
        self.sma_50_greater_than_sma_200 = self.sma_50.mean() > self.sma_200.all()
        self.rsi_above_70 = self.rsi.mean() > 70
        self.macd_above_signal = self.macd.mean() > self.signal.mean()
        self.adx_above_25 = self.adx.mean() > 25
        self.rsi_below_30 = self.rsi.mean() < 30
        self.macd_below_signal = self.macd.mean() < self.signal.mean()
        self.rsi_below_20 = self.rsi.mean() < 20
        if self.sma_50_greater_than_sma_200:
          st.markdown(f":green[SMA 50 is greater than SMA 200] is: {self.sma_50_greater_than_sma_200}")
          #st.write(f"SMA 50 is greater than SMA 200: {self.sma_50_greater_than_sma_200}")
        else:
            st.markdown(f":red[SMA 50 is greater than SMA 200] is: {self.sma_50_greater_than_sma_200}")
            #st.write(f"SMA 50 is greater than SMA 200: {self.sma_50_greater_than_sma_200}")
        if self.rsi_above_70:
            st.markdown(f":green[RSI is above 70] is: {self.rsi_above_70}")
            #st.write(f"RSI is above 70: {self.rsi_above_70}")
        else:
            st.markdown(f":red[RSI is above 70] is: {self.rsi_above_70}")
            #st.write(f"RSI is above 70: {self.rsi_above_70}")
        if self.macd_above_signal:
            st.markdown(f"green[MACD is above Signal] is: {self.macd_above_signal}")
        else:
            st.markdown(f"red[MACD is above Signal] is: {self.macd_above_signal}")
        if self.adx_above_25:
            st.markdown(f"green[ADX is above 25] is: {self.adx_above_25}")
        else:
            st.markdown(f"red[ADX is above 25] is: {self.adx_above_25}")
        if self.rsi_below_30:
            st.markdown(f"green[RSI is below 30] is: {self.rsi_below_30}")
        else:
            st.markdown(f"red[RSI is below 30] is: {self.rsi_below_30}")
        if self.macd_below_signal:
            st.markdown(f"green[MACD is below Signal] is: {self.macd_below_signal}")
        else:
            st.markdown(f"red[MACD is below Signal] is: {self.macd_below_signal}")
        if self.rsi_below_20:
            st.markdown(f"red[RSI is below 20] is: {self.rsi_below_20}")
        else:
            st.markdown(f"red[RSI is below 20] is: {self.rsi_below_20}")
        # Return the trend classification
        if self.sma_50_greater_than_sma_200 or self.rsi_above_70 or self.macd_above_signal or self.adx_above_25:
            return "Strong Bullish"
        elif self.sma_50_greater_than_sma_200 or self.rsi_below_30 or self.macd_below_signal or self.adx_above_25:
            return "Strong Bearish"
        elif self.sma_50_greater_than_sma_200 or self.rsi_above_70 or self.macd_above_signal:
            return "Weak Bullish"
        elif self.sma_50_greater_than_sma_200 or self.rsi_below_20 or self.macd_below_signal:
            return "Weak Bearish"
        else:
            return "Neutral"
  def techIndicators(self):
      self.df.rename(columns={'Open':'open','High':'high','Low':'low','Close':'close'},inplace=True)
      self.techDF['ADX']=abstract.ADX(self.df)
      self.techDF=pd.concat([self.techDF,abstract.AROON(self.df)],axis=1)
      self.techDF=pd.concat([self.techDF,abstract.BBANDS(self.df)],axis=1)
      self.techDF['EMA 20']=abstract.EMA(self.df,timeperiod=20)
      self.techDF=pd.concat([self.techDF,abstract.MACD(self.df)],axis=1)
      self.techDF['RSI']=abstract.RSI(self.df)
      self.techDF['SMA 25']=abstract.SMA(self.df,timeperiod=25)
      self.df.rename(columns={'open':'Open','high':'High','low':'Low','close':'Close'},inplace=True) # Revert to Original columns
      return self.techDF


