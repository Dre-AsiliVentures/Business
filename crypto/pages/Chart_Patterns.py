# Import the necessary libraries
import matplotlib.pyplot as plt
#from mpl_finance import candlestick_ohlc
import mplfinance as mpf
#from streamlit import caching
import streamlit as st
import sys
try:
    sys.path.append('/app/business')
    from crypto import main
    from Technical_Analysis import chart_patterns
except:  
    sys.path.append('/mount/src/business')
    from crypto import main
    from Technical_Analysis import chart_patterns
#sys.path.append('/app/business/fx')
import time
st.session_state['SupportResistance_Figure']=None
candlestickfigure_placeholder = st.empty()
try:
    if st.session_state['CurrencyPair'] is not None and st.session_state['DataFrame'] is not None:
        #@st.cache_resource
        def support_Resistance():
            # Create a placeholder for the dataframe
            data_placeholder = st.empty()
            status_displayed = False  # Flag to track whether status message has been displayed
            # Continuously update the data by fetching new data from the API
            #lookback=st.slider(label="Sensitivity in Percentage %", min_value=1, max_value=100, value=25, step=1)
            while True:
                data_placeholder.dataframe(st.session_state['DataFrame'].describe())
                # Display status message only once
                chart_pattern=chart_patterns.Pattern(data=st.session_state['DataFrame'])
                support_resistance_lines=list(chart_pattern.support_resistance())
                #support_resistance_lines=list(chart_pattern.support_resistance(int(lookback)))
                st.session_state['support_resistance_lines'] = support_resistance_lines
                fig=mpf.plot(st.session_state['DataFrame'],type='candle',volume=True,style='binance',hlines=dict(hlines=support_resistance_lines,colors=['g','r'],linestyle='-.'))
                st.session_state['SupportResistance_Figure']=fig
                time.sleep(2)  # Wait for 1 second
                break
        #st.set_option('deprecation.showPyplotGlobalUse', False)
        st.title('Chart Patterns :chart:')
        st.header(":green[Support] and :red[Resistance] Levels")
        support_Resistance()
        if st.session_state['SupportResistance_Figure'] is not None:
            candlestickfigure_placeholder.pyplot(st.session_state['SupportResistance_Figure'])
        with st.expander("More info on Support and Resistance"):
            #st.info("Sensitivity is the % of data the system looks back to find support and resistance.")
            # Access support_resistance_lines from st.session_state
            support_level = st.session_state.support_resistance_lines[0]
            resistance_level = st.session_state.support_resistance_lines[1]
            #st.markdown(f"**Support Level** is: {support_level}", unsafe_allow_html=True)
            st.markdown(f":green[Support Level] is: {support_level}", unsafe_allow_html=True)
            st.markdown(f":red[Resistance Level] is: {resistance_level}", unsafe_allow_html=True)
    else:
        st.warning("Choose your desired coin from the CryptoAnalysis page to proceed!!")
        pass

except Exception as e:
    st.warning(e)


