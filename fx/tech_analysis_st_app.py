import sys
#from ta import trend
#sys.path.append('/app/business/fx')
sys.path.append('/app/business')
from fx import main
import matplotlib.pyplot as plt
import numpy as np
import streamlit as st
from technical_analysis import TIndicators
#c=np.random.randn(100)
#macd=trend.MACD(close=c,window_slow=26,window_fast=12,window_sign=9)
currencypair=st.selectbox("Select you investment currency pair: ",main.maj_forex_pairs)
#st.write(results)
selected_interval = st.slider('Select an interval:', 0, len(main.intervals)-1, format_func=lambda i: main.labels[i])
# Map the selected value to the corresponding interval
selected_value = main.intervals[selected_interval]
data = main.collect_forex_data(f"{currencypair}=X",selected_interval)
ta=TIndicators(data['Open'])
results=ta.MACD()
st.write(results)
#st.write(data)
st.write(f"Investment yako inabamba enyewe {currencypair}")
