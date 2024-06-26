# Import the necessary libraries
import matplotlib.pyplot as plt
#from mpl_finance import candlestick_ohlc
import mplfinance as mpf
import os
import pandas as pd
import requests
#from streamlit import caching
import streamlit as st
import sys
try:
    sys.path.append('/app/business')
    from Technical_Analysis import chart_patterns
    from crypto import main
except: 
    sys.path.append('/mount/src/business')
    from Technical_Analysis import chart_patterns
    #from crypto import main

#sys.path.append('/app/business/fx')
import time
from tradingpatterns import tradingpatterns
import tweepy
st.session_state['SupportResistance_Figure']=None

if st.session_state['CurrencyPair'] is not None and st.session_state['DataFrame'] is not None:
    currency_pair = st.session_state.get('CurrencyPair')
    image_file_path = f"{currency_pair}_chart.png"
    def support_Resistance():
        status_displayed = False  # Flag to track whether status message has been displayed
        # Continuously update the data by fetching new data from the API
        #lookback=st.slider(label="Sensitivity in Percentage %", min_value=1, max_value=100, value=25, step=1)
        # Display status message only once
        chart_pattern=chart_patterns.Pattern(data=st.session_state['DataFrame'])
        support_resistance_lines=list(chart_pattern.support_resistance())
        #support_resistance_lines=list(chart_pattern.support_resistance(int(lookback)))
        st.session_state['support_resistance_lines'] = support_resistance_lines
        fig, axlist=mpf.plot(st.session_state['DataFrame'],type='candle',title=f"{st.session_state['CoinPair']} {st.session_state['Interval']} Support Resistance Plot",
                     volume=True,style='binance',
                     hlines=dict(hlines=support_resistance_lines,colors=['g','r'],linestyle='-.'),
                     savefig=image_file_path,returnfig=True)
        axlist[-2].set_xlabel=f"{st.session_state['Start_Date']} to {st.session_state['End_Date']}"
        #candlestickfigure_placeholder.pyplot(fig)
        #st.session_state['support']=lambda round(float(support_resistance_lines[0]), 2): round(float(support_resistance_lines[0]),2) if support_resistance_lines[0]>1 else round(support_resistance_lines[0],4)
        support=lambda x=support_resistance_lines[0]: round(float(x), 2) if float(x) > 1 else round(float(x), 4)
        st.session_state['support']=support()
        resistance=lambda x=support_resistance_lines[1]: round(float(x), 2) if float(x) > 1 else round(float(x), 4)
        st.session_state['resistance']=resistance()
        #st.pyplot(fig)
        #plt.savefig(f"{image_file_path}",dpi=1400)
        st.image(image_file_path)
        time.sleep(2)  # Wait for 2 seconds
    def send_telegram_Message():
        bot_token=st.secrets['bot_token']
        chat_id=st.secrets['chat_id']
        url = f'https://api.telegram.org/bot{bot_token}/sendPhoto' # URL to the Telegram Bot API for sending photos
        #caption = f"Coin Pair:{st.session_state['CurrencyPair']}\nStart Date: {st.session_state['Start_Date']} to {st.session_state['End_Date']}\nInterval={st.session_state['Interval']}\nSupport Level: {st.session_state['support']}\nResistance Level: {st.session_state['resistance']}\n{st.session_state['DataFrame'].iloc[-1]}"
        caption = f"Coin Pair: {st.session_state['CurrencyPair']}\nCrypto Token: ${st.session_state['Token']}\nCrypto Token Category: {st.session_state['TokenCategory']}\nStart Date: {st.session_state['Start_Date']} to {st.session_state['End_Date']}\nInterval={st.session_state['Interval']}\nSupport Level: {st.session_state['support']}\nResistance Level: {st.session_state['resistance']}\n#CryptoGuideBotTrading"
        payload = {'chat_id': chat_id,'caption': caption}     
        files = {'photo': open(image_file_path, 'rb')} # Prepare the payload
        response = requests.post(url, data=payload, files=files) # Send the photo
        if response.status_code == 200:
            st.toast('Chart Patterns available!')
            if os.path.exists(image_file_path):
                os.remove(image_file_path)
        else:
            #st.toast('Failed to send photo. Status code:', response.status_code)
            st.toast(response.text)
    def send_twitter_Message():
        apiKey= st.secrets['apiKey']
        apiSecret=st.secrets['apiSecret']
        bearerToken=st.secrets['bearerToken']
        accessToken=st.secrets['accessToken']
        accessSecret=st.secrets['accessSecret']
        client = tweepy.Client(bearer_token=bearerToken,consumer_key=apiKey,consumer_secret=apiSecret,access_token=accessToken,access_token_secret=accessSecret)
        auth = tweepy.OAuthHandler(apiKey, apiSecret)
        auth.set_access_token(accessToken,accessSecret)
        api = tweepy.API(auth)
        media = api.media_upload(filename=image_file_path)
        media_id = media.media_id
        caption = f"Coin Pair: {st.session_state['CurrencyPair']}\nCrypto Token: ${st.session_state['Token']}\nCrypto Token Category: {st.session_state['TokenCategory']}\nStart Date: {st.session_state['Start_Date']} to {st.session_state['End_Date']}\nInterval={st.session_state['Interval']}\nSupport Level: {st.session_state['support']}\nResistance Level: {st.session_state['resistance']}\n#CryptoTradingGuideBot."
        client.create_tweet(media_ids=[media_id], text=caption)
    #st.set_option('deprecation.showPyplotGlobalUse', False)
    with st.container():
        st.title(f"{st.session_state['CurrencyPair']} Chart Pattern from {st.session_state['Start_Date']} to {st.session_state['End_Date']} :chart:")
        df_placeholder = st.empty() # Create a placeholder for the dataframe
        data_placeholder = st.empty() # Create a placeholder for the dataframe descriptive stats
        with df_placeholder.expander("View Candlestick Data"):
            st.dataframe(st.session_state['DataFrame'])
        with data_placeholder.expander("Descriptive Statistics"):
            st.dataframe(st.session_state['DataFrame'].describe())
        chart_patterns_placeholder = st.empty() # Create a placeholder for the Chart Patterns
        st.header(":green[Support] and :red[Resistance] Levels")
        candlestickfigure_placeholder = st.empty() # Create a placeholder for the candlestickfigure
        support_Resistance()
        with st.expander("More info on Support and Resistance"):
            #st.info("Sensitivity is the % of data the system looks back to find support and resistance.")
            # Access support_resistance_lines from st.session_state
            support_level = st.session_state['support']
            resistance_level = st.session_state['resistance']
            #st.markdown(f"**Support Level** is: {support_level}", unsafe_allow_html=True)
            st.markdown(f":green[Support Level] is: {support_level}", unsafe_allow_html=True)
            st.markdown(f":red[Resistance Level] is: {resistance_level}", unsafe_allow_html=True)
            #st.write(f"The last candlestick is {candlestickID.candlestick_Pattern(len(st.session_state['DataFrame'])-1)[0]}")
            #st.write(f"The last candlestick trend pattern is {candlestickID.candlestick_Pattern(len(st.session_state['DataFrame'])-1)[1]}")
            # st.session_state['DataFrame']
        candlestickID=chart_patterns.Pattern(data=st.session_state['DataFrame'])
        candlestickDF=pd.DataFrame(columns=['Date', 'Pattern','Trend'])
        for dfindex in range(len(st.session_state['DataFrame'])):
            patternsID=candlestickID.candlestick_Pattern(dfindex)
            #candlestickDF.at[dfindex,'Date']=st.session_state['DataFrame'].iloc[dfindex]['Date']
            candlestickDF.at[dfindex,'Date']=st.session_state['DataFrame'].index[dfindex]
            #candlestickDF.at[dfindex,'Pattern']=patternsID.max_pattern
            pattern_name=str(patternsID[0])
            candlestickDF.at[dfindex,'Pattern']=candlestickID.candlestick_dict[pattern_name]
            candlestickDF.at[dfindex,'Trend']=patternsID[2]
        with chart_patterns_placeholder.expander("View Chart Patterns"):
            data=st.session_state["DataFrame"]
            head_shoulder=tradingpatterns.detect_head_shoulder(df=data)
            multiple_top_bottom=tradingpatterns.detect_multiple_tops_bottoms(df=data)
            triangle_pattern=tradingpatterns.detect_triangle_pattern(df=data)
            wedge_pattern=tradingpatterns.detect_wedge(df=data)
            double_topbottom_pattern=tradingpatterns.detect_double_top_bottom(df=data)
            data=data[['head_shoulder_pattern','multiple_top_bottom_pattern','triangle_pattern','wedge_pattern','double_pattern']]
            st.write(data)
        candlestickpatterns_placeholder = st.empty() # Create a placeholder for the candlestick Patterns Dataframe 
        with candlestickpatterns_placeholder.expander("View Candlestick Patterns"):
            st.dataframe(candlestickDF.dropna().reset_index().drop(columns=['index']))
            
    send_twitter_Message()
    send_telegram_Message()
    
    
